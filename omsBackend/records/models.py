# -*- coding: utf-8 -*-
# author: itimor

from django.db import models


class Record(models.Model):
    name = models.CharField(max_length=30, verbose_name=u"名称")
    method = models.CharField(max_length=30, verbose_name=u"请求方式")
    before = models.CharField(max_length=500, verbose_name=u"修改前内容")
    after = models.CharField(max_length=500, verbose_name=u"修改后内容")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name=u'修改时间')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u'记录'
        verbose_name_plural = u'记录'
