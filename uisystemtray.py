from autostart import AutoStart

import pystray
from PIL import Image
from threading import Thread

class SystemTray(Thread):
    def __init__(self, title: str, author: str, version: str, icon: str):
        super().__init__()
        self.title = title
        self.author = author
        self.version = version
        self.icon = icon
        self.autoStartStatus = False
        self.tray = None
        self.extraMenuItemList: list[pystray.MenuItem] = []

    def toggleAutoStart(self):
        """
        切换自启动状态
        """
        if self.autoStartStatus:
            AutoStart.unsetAutoStart()
        else:
            AutoStart.setAutoStart()
        self.autoStartStatus = AutoStart.checkAutoStart()

        # 刷新勾选状态
        self.updateAutoStartMenu()

    # 更新菜单勾选
    def updateAutoStartMenu(self):
        # 重新构建菜单（pystray 不支持直接修改，只能替换）
        versionMenu = pystray.MenuItem(f'版本：{self.version}', None)
        authorMenu = pystray.MenuItem(f'作者：{self.author}', None)
        titleMenu = pystray.Menu(versionMenu, authorMenu)
        titleMenuItem = pystray.MenuItem(self.title, titleMenu)

        # 勾选状态
        autoStartMenuItem = pystray.MenuItem(
            '开机自启动',
            self.toggleAutoStart,
            lambda item: self.autoStartStatus,
        )

        rootMenu = pystray.Menu(
            titleMenuItem,
            autoStartMenuItem,
            *self.extraMenuItemList
        )

        self.tray.menu = rootMenu
        self.tray.update_menu()

    def addMenuItemList(self, menuItemList: list[pystray.MenuItem]):
        self.extraMenuItemList = menuItemList

    def run(self):
        # 初始化状态
        self.autoStartStatus = AutoStart.checkAutoStart()

        # 初始菜单（先创建一次）
        versionMenu = pystray.MenuItem(f'版本：{self.version}', None)
        authorMenu = pystray.MenuItem(f'作者：{self.author}', None)
        titleMenu = pystray.Menu(versionMenu, authorMenu)
        titleMenuItem = pystray.MenuItem(self.title, titleMenu)

        autoStartMenuItem = pystray.MenuItem(
            '开机自启动',
            self.toggleAutoStart,
            lambda item: self.autoStartStatus
        )

        rootMenu = pystray.Menu(
            titleMenuItem,
            autoStartMenuItem,
            *self.extraMenuItemList
        )

        iconImg = Image.open(self.icon)
        self.tray = pystray.Icon(self.title, iconImg, self.title, rootMenu)
        self.tray.run()

    def stopSystemTray(self):
        if self.tray:
            self.tray.stop()
