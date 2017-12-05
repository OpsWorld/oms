# -*- coding: utf-8 -*-
# author: itimor

from dry_rest_permissions.generics import allow_staff_or_superuser, authenticated_users
from django.db import models

from users.models import User
from menus.models import Firstmenu, Secondmenu, MenuMeta


class UserMenuPerms(models.Model):
    user = models.ForeignKey(User, unique=True)
    firstmenus = models.ManyToManyField(Firstmenu, verbose_name=u'一级菜单')
    seaondmenus = models.ManyToManyField(Secondmenu, verbose_name=u'二级菜单')

    def __str__(self):
        return self.user

    class Meta:
        verbose_name = u'用户菜单权限'
        verbose_name_plural = u'用户菜单权限'


