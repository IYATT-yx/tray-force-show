"""
file: uisystemtray.py
description: 系统托盘
author: IYATT-yx
copyright:  Copyright (c) 2025-2026 IYATT-yx.
            Licensed under the MIT License. See LICENSE file in the project root for full license information.
"""
import pystray
from PIL import Image
from threading import Thread

from pystartup import StartupManager

import base
from buildtime import buildTime

class SystemTray(Thread):
    def __init__(self, title: str, icon: str):
        super().__init__()
        self.title = title
        self.icon = icon
        self.autoStartStatus = False
        self.tray = None
        self.extraMenuItemList: list[pystray.MenuItem] = []

        StartupManager.init(base.project, mode=StartupManager.MODE_REGISTRY)

    def onClickAutoStart(self, icon, item):
        if self.autoStartStatus:
            StartupManager.unsetStartup()
        else:
            StartupManager.setStartup()
        
        self.updateAutoStartMenu(first=False)

    # 更新菜单勾选
    def updateAutoStartMenu(self, first: bool = False):
        # 获取最新自启动状态
        self.autoStartStatus, _ = StartupManager.checkStartup()

        # 信息
        infoMenuItem = pystray.MenuItem(
            f'{self.title} By IYATT-yx {buildTime}',
            None
        )

        # 勾选状态
        autoStartMenuItem = pystray.MenuItem(
            '开机自启动',
            self.onClickAutoStart,
            lambda item: self.autoStartStatus,
        )

        rootMenu = pystray.Menu(
            infoMenuItem,
            autoStartMenuItem,
            *self.extraMenuItemList
        )

        if first:
            iconImg = Image.open(self.icon)
            self.tray = pystray.Icon(self.title, iconImg, self.title, rootMenu)
            self.tray.run()
        else:
            if self.tray:
                self.tray.menu = rootMenu
                self.tray.update_menu()

    def addMenuItemList(self, menuItemList: list[pystray.MenuItem]):
        self.extraMenuItemList = menuItemList

    def run(self):
        self.updateAutoStartMenu(first=True)

    def stopSystemTray(self):
        if self.tray:
            self.tray.stop()
