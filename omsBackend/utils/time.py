# -*- coding: utf-8 -*-
# author: itimor

import time
import datetime


def utc2local(utc_st):
    """
    UTC时间转本地时间 +8:00
    """
    now_stamp = time.time()
    local_time = datetime.datetime.fromtimestamp(now_stamp)
    utc_time = datetime.datetime.utcfromtimestamp(now_stamp)
    offset = local_time - utc_time
    local_st = utc_st + offset
    return local_st


def local2utc(local_st):
    """
    本地时间转UTC时间 -8:00
    """
    time_struct = time.mktime(local_st.timetuple())
    utc_st = datetime.datetime.utcfromtimestamp(time_struct)
    return utc_st