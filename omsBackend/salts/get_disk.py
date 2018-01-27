# -*- coding: utf-8 -*-
# author: itimor

import psutil


def get_disk_info():
    grains = {}
    data = psutil.disk_partitions()
    disks = []
    for disk in data:
        diskname = disk.mountpoint
        disktotal = psutil.disk_usage(disk.mountpoint).total / 1024 / 1024 / 1024
        disks.append('{} {}GB'.format(diskname, int(disktotal)))
    grains["disk_info"] = disks
    return grains


print(get_disk_info())
