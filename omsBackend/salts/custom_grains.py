# -*- coding: utf-8 -*-
# author: itimor

import platform
import psutil
import socket
import cpuinfo
import re
import os


class GetGrains(object):
    def __init__(self):
        self.windows = (platform.system() == "Windows")
        self.linux = (platform.system() == "Linux")
        self.grains = {}

    def get_hostname_info(self):
        return socket.gethostname()

    def get_ip_info(self):
        if self.windows:
            data = socket.gethostbyname_ex(socket.gethostname())
            return ','.join(data[2])
        elif self.linux:
            ips = os.popen('ip addr').read()
            data = re.findall('inet ([\d+\.]{3,}\d+)', ips)
            return '/'.join(data)

    def get_os_info(self):
        return platform.platform()

    def get_cpu_info(self):
        data = cpuinfo.get_cpu_info()
        return '{} * {}'.format(data["brand"], data["count"])

    def get_memory_info(self):
        data = psutil.virtual_memory()
        return '{}GB'.format(int(data.total / 1024 / 1024 / 1024))

    def get_disk_info(self):
        data = psutil.disk_partitions()
        disks = []
        for disk in data:
            diskname = disk.mountpoint
            disktotal = psutil.disk_usage(disk.mountpoint).total / 1024 / 1024 / 1024
            dsk = dict()
            dsk[diskname] = '{}GB'.format(int(disktotal))
            disks.append(dsk)
        return disks


def main():
    grains = dict()
    get_grains = GetGrains()
    # grains["hostname_info"] = get_grains.get_hostname_info()
    # grains["ip_info"] = get_grains.get_ip_info()
    # grains["os_info"] = get_grains.get_os_info()
    # grains["cpu_info"] = get_grains.get_cpu_info()
    # grains["memory_info"] = get_grains.get_memory_info()
    grains["disk_info"] = get_grains.get_disk_info()
    return grains