# -*- coding: utf-8 -*-
# author: itimor

from websocket import create_connection

ws = create_connection("ws://192.168.6.99:8001/salt/cmdrun/")
print("Sending 'Hello, World'...")
ws.send("Hello, World")
print("Sent")
print("Reeiving...")
result =  ws.recv()
print("Received '%s'" % result)
ws.close()