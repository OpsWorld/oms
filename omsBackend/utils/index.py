# -*- coding: utf-8 -*-
# author: itimor

import datetime


def create_time_pid():
    pid = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    return pid


if __name__ == '__main__':
    print(create_time_pid())

