# -*- coding: utf-8 -*-
# author: itimor

from __future__ import absolute_import, unicode_literals  # 目的是拒绝隐士引入，celery.py和celery冲突。
import os
from celery import Celery
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dailyblog.settings")

# 创建celery应用
app = Celery('omsBackend')
# You can pass the object directly here, but using a string is better since then the worker doesn’t have to serialize the object.
app.config_from_object('django.conf:settings')
# 如果在工程的应用中创建了tasks.py模块，那么Celery应用就会自动去检索创建的任务。比如你添加了一个任务，在django中会实时地检索出来。
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)