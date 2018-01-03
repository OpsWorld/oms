# -*- coding: utf-8 -*-
# author: kiven

from django.db import models
from users.models import User, Group
from worktickets.models import TicketType


class Wiki(models.Model):
    title = models.CharField(max_length=100, blank=True, verbose_name=u'标题')
    type = models.ForeignKey(TicketType, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=u'类型')
    content = models.TextField(verbose_name=u'内容')
    create_user = models.ForeignKey(User, verbose_name=u'创建者')
    create_group = models.ManyToManyField(Group, null=True, blank=True, verbose_name=u'部门')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name=u'创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name=u'更新时间')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = u'wiki'
        verbose_name_plural = u'wiki'