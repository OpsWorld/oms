# -*- coding: utf-8 -*-
# author: kiven

from django.db import models

class Firstmenu(models.Model):
    title = models.CharField(max_length=100, blank=True, unique=True, verbose_name=u'菜单中文')
    name = models.CharField(max_length=100, blank=True, unique=True, verbose_name=u'菜单名')
    path = models.CharField(max_length=100, blank=True, verbose_name=u'菜单实际路径')
    component = models.CharField(max_length=100, blank=True, verbose_name=u'菜单指向页面')
    icon = models.CharField(max_length=100, blank=True, verbose_name=u'菜单图标')
    redirect = models.CharField(max_length=100, blank=True, verbose_name=u'菜单rewrite路径')
    hidden = models.BooleanField(default=False, verbose_name=u'是否隐藏菜单')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = u'一级菜单'
        verbose_name_plural = u'一级菜单'

class Secondmenu(models.Model):
    parent = models.ForeignKey("Firstmenu", verbose_name=u'上级菜单')
    title = models.CharField(max_length=100, blank=True, unique=True, verbose_name=u'菜单中文')
    name = models.CharField(max_length=100, blank=True, unique=True, verbose_name=u'菜单名')
    path = models.CharField(max_length=100, blank=True, verbose_name=u'菜单实际路径')
    component = models.CharField(max_length=100, blank=True, verbose_name=u'菜单指向页面')
    hidden = models.BooleanField(default=False, verbose_name=u'是否隐藏菜单')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = u'二级菜单'
        verbose_name_plural = u'二级菜单'


class Element(models.Model):
    parent = models.ForeignKey("Secondmenu", verbose_name=u'所属菜单')
    name = models.CharField(max_length=100, blank=True, verbose_name=u'菜单元素')
    code = models.CharField(max_length=100, blank=True, verbose_name=u'元素code')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u'菜单元素'
        verbose_name_plural = u'菜单元素'

    def save(self, *args, **kwargs):
        parent = Secondmenu.objects.get(title=self.parent)
        self.name = '{}-{}'.format(parent.title,self.name)
        self.code = '{}:{}'.format(parent.name,self.code)
        super(Element, self).save(*args, **kwargs)
