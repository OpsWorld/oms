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

a = [{'tw-btj-thirdpay-prod-02': {'num_cpus': 16, 'disk_info': ['C:\\ 488.18GB', 'D:\\ 443.23GB'], 'cpu_model': 'Intel(R) Xeon(R) CPU           L5630  @ 2.13GHz', 'memory_info': '15.99GB', 'ipv4': ['192.168.88.27'], 'osfinger': 'Windows-2008ServerR2'}, 'tw-btj-thirdpay-prod-01': {'num_cpus': 16, 'disk_info': ['C:\\ 200.00GB', 'D:\\ 731.41GB'], 'cpu_model': 'Intel(R) Xeon(R) CPU           L5630  @ 2.13GHz', 'memory_info': '15.99GB', 'ipv4': ['192.168.88.16'], 'osfinger': 'Windows-2008ServerR2'}}]

host = dict()
for k, v in a[0].items():
    print(k, v)
    print("\nccc")

