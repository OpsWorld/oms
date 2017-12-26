# -*- coding: utf-8 -*-
# author: itimor

from omsBackend import celery_app
from utils.sendskype import skype_bot
from utils.sendmail import send_mail

@celery_app.task
def send_to_skype(user,content):
    print(content)
    skype_bot(user, content)

@celery_app.task
def send_to_mail(to_list, cc_list, sub, content):
    print(sub)
    send_mail(to_list, cc_list, sub, content)
