# -*- coding: utf-8 -*-
# author: itimor

from django.db import models
from menus.models import Firstmenu, Secondmenu, Element
from users.models import User, Group
from hosts.models import Host, HostGroup


class UserMenuPerms(models.Model):
    group = models.CharField(max_length=64, unique=True, verbose_name=u'部门')
    firstmenus = models.ManyToManyField(Firstmenu, verbose_name=u'一级菜单')
    secondmenus = models.ManyToManyField(Secondmenu, verbose_name=u'二级菜单')
    elements = models.ManyToManyField(Element, verbose_name=u'菜单元素')

    def __str__(self):
        return self.group

    class Meta:
        verbose_name = u'用户菜单权限'
        verbose_name_plural = u'用户菜单权限'


class UserHostPerms(models.Model):
    name = models.CharField(max_length=128, unique=True, blank=True)
    # users = models.ManyToManyField(User, related_name='asset_permissions', blank=True)
    usergroups = models.ForeignKey(Group, models.SET_NULL, blank=True, null=True,
                                   related_name='usergroups_hostpermissions')
    hosts = models.ManyToManyField(Host, related_name='hosts_hostpermissions', blank=True)

    # hostgroups = models.ManyToManyField(HostGroup, related_name='granted_by_permissions', blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u'用户主机权限'
        verbose_name_plural = u'用户主机权限'

    def save(self, *args, **kwargs):
        self.name = '{}主机权限'.format(self.usergroups)
        super(UserHostPerms, self).save(*args, **kwargs)
