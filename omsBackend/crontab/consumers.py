# -*- coding: utf-8 -*-
# author: itimor

import json
import os
from crontab.cmdrun import run
# from salts.models import SaltCmdrun   #命令记录

salt_log = '/tmp/salt/'
os.popen('mkdir -p {}'.format(salt_log))


def cmdrun_receive(message):
    text = message.content['text']
    request = json.loads(text)
    user = request['user']
    hosts = request['hosts']
    cmd = request['cmd']

    # 命令记录
    # cmdrun = SaltCmdrun(user=user, hosts=hosts, cmd=cmd)
    # cmdrun.save()

    results = run(cmd).stdout
    for result in results:
        message.reply_channel.send({'text':result.decode('utf-8')}, True)
