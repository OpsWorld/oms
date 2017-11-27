# -*- coding: utf-8 -*-
# author: itimor

from channels.routing import route, include
from crontab.router import salt_routing

channel_routing = [
    include(salt_routing, path='^/salt'),
]