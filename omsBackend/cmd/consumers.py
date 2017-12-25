# -*- coding: utf-8 -*-
# author: kiven

import json
import os
from cmd.cmdrun import run
from utils.sendskype import skype_bot


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


def sendmessage_receive(message):
    text = message.content['text']
    request = json.loads(text)
    to_user = request["user"]
    content = request["title"] + '\n' + request["message"]
    print(request)
    #results = skype_bot(to_user,content).stdout
    #for result in results:
    message.reply_channel.send({'text':'111'}, True)
