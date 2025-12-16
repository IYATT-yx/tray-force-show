from buildtime import buildTime

import os

project = 'tray-force-show'
name = '强制显示托盘图标工具'
author = 'IYATT-yx iyatt@iyatt.com'
version = buildTime
icon = os.path.join(os.path.dirname(__file__), 'icon.ico')
