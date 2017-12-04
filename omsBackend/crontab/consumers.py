# -*- coding: utf-8 -*-
# author: kiven

import json
import os
from crontab.cmdrun import run
# from salts.models import SaltCmdrun   #命令记录
from omsBackend.settings import  SEND_MAIL_CMD

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

def sendmail_receive(message):
    text = message.content['text']
    request = json.loads(text)
    to_list = request['to_list']
    sub = request['sub']
    context = request['context']
    cmd = '{} {} {} {}'.format(SEND_MAIL_CMD,to_list,sub,context)
    print(cmd)

    # results = run(cmd).stdout
    # for result in results:
    #     message.reply_channel.send({'text':result.decode('utf-8')}, True)
