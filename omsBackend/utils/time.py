# -*- coding: utf-8 -*-
# author: itimor

d = '2017-12-06 12:58:20.097417'
#
# import datetime
# dateStr = '2013-10-10 23:40:00.22'
# datetimeObj = datetime.datetime.strptime(dateStr, "%Y-%m-%d %H:%M:%S")

import datetime
now = datetime.datetime.now()
print(now)
otherStyleTime = d.strftime("%Y-%m-%d %H:%M:%S")
print(otherStyleTime)
