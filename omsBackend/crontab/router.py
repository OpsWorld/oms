# -*- coding: utf-8 -*-
# author: itimor

from channels.routing import route
from salts.consumers import cmdrun_receive, editfile_receive

salt_routing = [
    route('websocket.receive',cmdrun_receive, path='/cmdrun/'),
    route('websocket.receive',editfile_receive, path='/editfile/'),
]