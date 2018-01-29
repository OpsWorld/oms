# -*- coding: utf-8 -*-
# author: itimor

# import datetime
# import time
#
# # dateStr = '2013-10-10 23:40:00.22'
# # datetimeObj = datetime.datetime.strptime(dateStr, "%Y-%m-%d %H:%M:%S")
#
# s_time = datetime.datetime.now()
# time.sleep(5)
# e_time = datetime.datetime.now()
#
# print((e_time-s_time).seconds/3600)

a = {'bj-aa-02': {'osfinger': 'Windows-7', 'memory_info': '15.87 GB', 'ipv4': ['1.1.1.1', '192.168.3.215', '192.168.10.1'], 'disk_info': ['C:\\ 120.00 GB', 'D:\\ 447.13 GB', 'E:\\ 103.57 GB'], 'cpu_model': 'Intel(R) Core(TM) i7-4790 CPU @ 3.60GHz'}, 'sh-aa-01': {'osfinger': 'CentOS Linux-7', 'memory_info': '3.69 GB', 'ipv4': ['10.10.10.1', '127.0.0.1', '172.17.0.1', '192.168.6.99'], 'disk_info': ['/ 95.58 GB', '/boot 496.67 MB'], 'cpu_model': 'Intel(R) Core(TM) i7-4790 CPU @ 3.60GHz'}}

host = {}
for k, v in a.items():
    host['hostname'] = k
    host['os'] = v['osfinger']

print(host)