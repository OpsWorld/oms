# -*- coding: utf-8 -*-
# author: kiven

from django.db import models
from users.models import User


class Firstmenu(models.Model):
    name = models.CharField(max_length=100, blank=True, verbose_name=u'菜单名')
    path = models.CharField(max_length=100, blank=True, verbose_name=u'菜单实际路径')
    component = models.CharField(max_length=100, blank=True, verbose_name=u'菜单指向页面')
    icon = models.CharField(max_length=100, blank=True, verbose_name=u'菜单图标')
    redirect = models.CharField(max_length=100, blank=True, verbose_name=u'菜单rewrite路径')
    hidden = models.BooleanField(default=True, verbose_name=u'是否显示菜单')
    meta = models.ManyToManyField("MenuMate", blank=True, null=True, verbose_name=u'扩展属性')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u'一级菜单'
        verbose_name_plural = u'一级菜单'

class Secondmenu(models.Model):
    parent = models.ForeignKey("Firstmenu", blank=True, null=True, verbose_name=u'父菜单')
    name = models.CharField(max_length=100, blank=True, verbose_name=u'菜单名')
    path = models.CharField(max_length=100, blank=True, verbose_name=u'菜单实际路径')
    component = models.CharField(max_length=100, blank=True, verbose_name=u'菜单指向页面')
    hidden = models.BooleanField(default=True, verbose_name=u'是否显示菜单')
    mate = models.ManyToManyField("MenuMate", blank=True, null=True, verbose_name=u'扩展属性')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u'二级菜单'
        verbose_name_plural = u'二级菜单'


class MenuMeta(models.Model):
    name = models.CharField(max_length=100, blank=True, verbose_name=u'菜单属性')
    action = models.CharField(max_length=100, blank=True, verbose_name=u'属性动作')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u'菜单属性'
        verbose_name_plural = u'菜单属性'
