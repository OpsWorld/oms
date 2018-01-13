# -*- coding: utf-8 -*-
# author: itimor

from omsBackend import celery_app
from utils.sendskype import skype_bot
from utils.sendmail import send_mail
from utils.saltrun import salt_run

@celery_app.task
def send_to_skype(user,content):
    print(content)
    skype_bot(user, content)

@celery_app.task
def send_to_mail(to_list, cc_list, sub, content):
    print(sub)
    send_mail(to_list, cc_list, sub, content)

@celery_app.task
def salt_run_cmd(hosts,cmd,deploy_path):
    from time import sleep
    for i in range(10):
        sleep(1)
        print(i)
        print(hosts, cmd, deploy_path)
        salt_run(hosts,cmd,deploy_path)
        return {'status': 'success'}
    return {'status': 'deploy'}