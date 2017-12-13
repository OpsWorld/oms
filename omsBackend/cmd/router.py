# -*- coding: utf-8 -*-
# author: kiven

from channels.routing import route
from cmd.consumers import cmdrun_receive

salt_routing = [
    route('websocket.receive',cmdrun_receive, path='/cmdrun/'),
]
