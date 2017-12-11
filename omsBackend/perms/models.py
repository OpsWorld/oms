# -*- coding: utf-8 -*-
# author: itimor

from django.db import models
from menus.models import Firstmenu, Secondmenu, Element
from users.models import Group

class UserMenuPerms(models.Model):
    group = models.OneToOneField(Group, verbose_name=u'部门')
    firstmenus = models.ManyToManyField(Firstmenu, verbose_name=u'一级菜单')
    secondmenus = models.ManyToManyField(Secondmenu, verbose_name=u'二级菜单')
    elements = models.ManyToManyField(Element, verbose_name=u'菜单元素')

    def __str__(self):
        return self.group

    class Meta:
        verbose_name = u'用户菜单权限'
        verbose_name_plural = u'用户菜单权限'


