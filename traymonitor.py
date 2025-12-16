import threading
import winreg
import win32api
import win32con
import win32event
import win32security

class TrayMonitor(threading.Thread):
    REG_NOTIFY_CHANGE_NAME = 0x00000001
    REG_NOTIFY_CHANGE_LAST_SET = 0x00000004

    def __init__(self):
        super().__init__()
        self.stopEvent = threading.Event()
        self.monitorThread = None

    def getCurrentUserSig(self) -> str:
        """
        获取当前用户SID

        Returns:
            str: 当前用户SID
        """
        token = win32security.OpenProcessToken(
            win32api.GetCurrentProcess(),
            win32con.TOKEN_QUERY
        )
        sid, _ = win32security.GetTokenInformation(token, win32security.TokenUser)
        return win32security.ConvertSidToStringSid(sid)

    def promoteAllTray(self):
        """
        修改注册表将所有托盘图标提升到最前
        """
        regPath = r'Control Panel\NotifyIconSettings'
        try:
            baseKey = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                regPath,
                0,
                winreg.KEY_READ | winreg.KEY_WRITE
            )
        except FileNotFoundError:
            return
        
        idx = 0
        while True:
            try:
                subkeyName = winreg.EnumKey(baseKey, idx)
            except OSError:
                break

            subpath = fr'{regPath}\{subkeyName}'
            try:
                subkey = winreg.OpenKey(
                    winreg.HKEY_CURRENT_USER,
                    subpath,
                    0,
                    winreg.KEY_READ | winreg.KEY_WRITE
                )

                try:
                    val, _ = winreg.QueryValueEx(subkey, 'IsPromoted')
                except FileNotFoundError:
                    val = 0

                if val != 1:
                    winreg.SetValueEx(subkey, 'IsPromoted', 0, winreg.REG_DWORD, 1)

                winreg.CloseKey(subkey)
            except :
                pass

            idx += 1
        winreg.CloseKey(baseKey)

    def waitForRegistryChange(self, sid: str):
        """
        监听注册表变化

        Args:
            sid (str): 当前用户SID
        """
        regPath = fr'{sid}\Control Panel\NotifyIconSettings'
        key = win32api.RegOpenKeyEx(
            win32con.HKEY_USERS,
            regPath,
            0,
            win32con.KEY_NOTIFY
        )

        event = win32event.CreateEvent(None, 0, 0, None)
        win32api.RegNotifyChangeKeyValue(
            key,
            True,
            TrayMonitor.REG_NOTIFY_CHANGE_LAST_SET | TrayMonitor.REG_NOTIFY_CHANGE_NAME,
            event,
            True
        )

        while True:
            result = win32event.WaitForSingleObject(event, 500)
            if self.stopEvent.is_set():
                return
            if result == win32event.WAIT_OBJECT_0:
                return


    def monitor(self):
        """
        监听注册表变化并提升托盘图标
        """
        sid = self.getCurrentUserSig()

        while not self.stopEvent.is_set():
            self.promoteAllTray()
            self.waitForRegistryChange(sid)

    def stopMonitor(self):
        """
        停止监听
        """
        self.stopEvent.set()
        if self.monitorThread is not None:
            self.monitorThread.join()

    def run(self):
        """
        启动托盘监听器
        """
        self.stopEvent.clear()
        monitorThread = threading.Thread(target=self.monitor)
        monitorThread.start()
