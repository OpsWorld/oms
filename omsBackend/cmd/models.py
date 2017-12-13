# -*- coding: utf-8 -*-
# author: itimor

from django.db import models
from users.models import User

class Cmdrun(models.Model):
    user = models.ForeignKey(User, verbose_name=u'执行用户')
    cmd = models.CharField(max_length=500, verbose_name=u'命令')
    hosts = models.CharField(max_length=110,  default='localhost', blank=True, verbose_name=u'执行机器')

    class Meta:
        verbose_name = u'cmdrun'
        verbose_name_plural = u'cmdrun'