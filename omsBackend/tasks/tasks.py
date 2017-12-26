# -*- coding: utf-8 -*-
# author: itimor

from omsBackend import celery_app
from utils.sendskype import skype_bot

@celery_app.task
def send_to_skype(user,content):
    print(user,content)
    skype_bot(user, content)