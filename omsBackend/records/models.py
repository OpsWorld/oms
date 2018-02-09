# -*- coding: utf-8 -*-
# author: itimor

from django.db import models

AddType = {
    0: 'manual',
    1: 'auto',
}


class Record(models.Model):
    name = models.CharField(max_length=30, verbose_name=u"app名称")
    type = models.CharField(max_length=3, choices=AddType.items(), default=0, verbose_name=u'添加类型')
    asset = models.CharField(max_length=30, null=True, blank=True,  verbose_name=u"资产对象")
    method = models.CharField(null=True, blank=True,  max_length=30, verbose_name=u"请求方式")
    before = models.TextField(default='{}', null=True, blank=True,  verbose_name=u"修改前内容")
    after = models.TextField(default='{}', null=True, blank=True,  verbose_name=u"修改后内容")
    diff = models.TextField(default=[], verbose_name=u"前后数据对比")
    create_user = models.CharField(max_length=10, default='kiven', verbose_name=u'创建者')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name=u'修改时间')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u'记录'
        verbose_name_plural = u'记录'
