# -*- coding: utf-8 -*-
# author: itimor

from django.db import models


class DnsApiKey(models.Model):
    name = models.CharField(max_length=20, unique=True, verbose_name=u'名称')
    key = models.CharField(max_length=201, verbose_name=u'api_key')
    secret = models.CharField(max_length=201, verbose_name=u'api_secret')
    desc = models.TextField(null=True, blank=True, verbose_name=u'备注')

    def __str__(self):
        return self.name
