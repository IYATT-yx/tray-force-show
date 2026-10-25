"""
file: application.py
description: 应用
author: IYATT-yx
copyright:  Copyright (c) 2025-2026 IYATT-yx.
            Licensed under the MIT License. See LICENSE file in the project root for full license information.
"""
from uisystemtray import SystemTray
from traymonitor import TrayMonitor
import base

import pystray

class Application:
    def __init__(self):
        self.tray = SystemTray(base.name, base.icon)
        self.monitor = TrayMonitor()

    def exit(self):
        self.monitor.stopMonitor()
        self.tray.stopSystemTray()

    def run(self):
        self.tray.addMenuItemList([
            pystray.MenuItem('退出', self.exit)
        ])
        self.tray.start()
        self.monitor.start()