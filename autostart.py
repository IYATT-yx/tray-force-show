import base

import winreg
from tkinter import messagebox
import sys
import os

AUTO_START_REG_PATH = r'Software\Microsoft\Windows\CurrentVersion\Run'

isPackaged: bool = not sys.argv[0].endswith('.py')
"""打包状态"""
startCommand = ('"' + sys.argv[0] + '"' if isPackaged else '"' + sys.executable + '" "' + os.path.abspath(sys.argv[0]) + '"')
"""启动命令"""

class AutoStart:
    @staticmethod
    def setAutoStart() -> bool:
        """设置开机自启动
        
        Returns:
            bool: 是否设置成功
        """
        try:
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                AUTO_START_REG_PATH,
                0,
                winreg.KEY_SET_VALUE
            )
            winreg.SetValueEx(key, base.project, 0, winreg.REG_SZ, startCommand)
            winreg.CloseKey(key)
            return True
        except Exception as e:
            messagebox.showerror('错误', f'设置开机自启动失败：{e}')
            return False

    @staticmethod
    def unsetAutoStart() -> tuple[bool, Exception | None | str]:
        """取消开机自启动

        Returns:
            bool: 是否取消成功
        """
        try:
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                AUTO_START_REG_PATH,
                0,
                winreg.KEY_SET_VALUE
            )
            winreg.DeleteValue(key, base.project)
            winreg.CloseKey(key)
            return True
        except FileNotFoundError:
            messagebox.showwarning('警告', '未设置开机自启动，无需取消')
            return True
        except Exception as e:
            messagebox.showerror('错误', f'取消开机自启动失败：{e}')
            return False

    @staticmethod
    def checkAutoStart() -> bool:
        """检查是否设置开机自启动

        Returns:
            bool: 是否设置自启动
        """
        try:
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                AUTO_START_REG_PATH,
                0,
                winreg.KEY_READ
            )
            value, _ = winreg.QueryValueEx(key, base.project)
            winreg.CloseKey(key)
            if value != startCommand: # 程序路径发生移动时，启动路径不匹配，也认为是没有设置自启动
                return False
            return True
        except FileNotFoundError:
            return False
        except Exception as e:
            messagebox.showerror('错误', f'检查开机自启动失败：{e}')
            return False
            

