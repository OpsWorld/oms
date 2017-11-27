# -*- coding: utf-8 -*-
# author: itimor

import json
import os
from salts.cmdrun import run
from salts.models import SaltCmdrun

salt_log = '/tmp/salt/'
os.popen('mkdir -p {}'.format(salt_log))


def cmdrun_receive(message):
    text = message.content['text']
    request = json.loads(text)
    user = request['user']
    hosts = request['hosts']
    cmd = request['cmd']

    cmdrun = SaltCmdrun(user=user, hosts=hosts, cmd=cmd)
    cmdrun.save()

    results = run(cmd).stdout
    for result in results:
        message.reply_channel.send({'text':result.decode('utf-8')}, True)


def cmdlog_receive(message):
    text = message.content['text']
    request = json.loads(text)
    cmd = request['cmd']

    results = run(cmd).stdout
    for result in results:
        message.reply_channel.send({'text':result.decode('utf-8')}, True)

def editfile_receive(message):
    text = json.loads(message.content['text'])
    request = text['data']
    filename = request['filename']

    if text['stream'] == 'read':
        cmd = 'cat {}'.format(filename)
        results = run(cmd).stdout
        for result in results:
            print(result)
            message.reply_channel.send({'text':result.decode('utf-8')}, True)
    else:
        results = request['results']
        with open(filename,'w') as fn:
            fn.write(results)
