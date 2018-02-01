# -*- coding: utf-8 -*-
# author: itimor

import psutil
import math


def get_grains_info():
    grains = {}
    disk_data = psutil.disk_partitions()
    disks = []
    for disk in disk_data:
        diskname = disk.mountpoint
        disktotal = convert_bytes(psutil.disk_usage(disk.mountpoint).total)
        disks.append('{} {}'.format(diskname, disktotal))
    grains["disk_info"] = disks

    mem_data = psutil.virtual_memory()
    total = convert_bytes(mem_data.total)
    grains["memory_info"] = total
    return grains


def convert_bytes(byte, lst=None):
    if lst is None:
        lst = ['Bytes', 'KB', 'MB', 'GB', 'TB', 'PB']
    # 求对数(对数：若 a**b = N 则 b 叫做以 a 为底 N 的对数)
    i = int(math.floor(math.log(byte, 1024)))

    if i >= len(lst):
        i = len(lst) - 1
    return ('%.2f' + lst[i]) % (byte / math.pow(1024, i))


print(get_grains_info())
