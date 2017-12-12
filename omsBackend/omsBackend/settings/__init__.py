# -*- coding: utf-8 -*-
# author: itimor

import platform

if platform.node() == "tboms":
    print("正式环境")
    from omsBackend.settings.base import *
    from omsBackend.settings.prod import *
else:
    print("开发环境")
    from omsBackend.settings.base import *
    from omsBackend.settings.dev import *