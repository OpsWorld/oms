# -*- coding: utf-8 -*-
# author: itimor

from websocket import create_connection

ws = create_connection("ws://oms.tb-gaming.local/ws/sendmessage/")
print("Sending 'Hello, World'...")
ws.send("Hello, World")
print("Sent")
print("Reeiving...")
result =  ws.recv()
print("Received '%s'" % result)
ws.close()