# -*- coding: utf-8 -*-
# author: itimor

from celery import task
from utils.sendskype import skype_bot
from utils.sendmail import send_mail

@task.task
def send_to_skype(user,content):
    print(content)
    skype_bot(user, content)

@task.task
def send_to_mail(to_list, cc_list, sub, content):
    print(sub)
    send_mail(to_list, cc_list, sub, content)