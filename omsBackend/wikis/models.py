# -*- coding: utf-8 -*-
# author: kiven

from django.db import models
from users.models import User, Group
from worktickets.models import TicketType

admin_groups = ['admin', 'OMS_Super_Admin']


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

    @staticmethod
    def has_read_permission(request):
        return True

    def has_object_read_permission(self, request):
        return True

    @staticmethod
    def has_write_permission(request):
        return True

    def has_object_write_permission(self, request):
        return True

    @staticmethod
    def has_update_permission(request):
        return True

    def has_object_update_permission(self, request):
        return True
        # groups = User.objects.get(username=request.user).groups.all()
        # groups_list = [group.name for group in self.create_group.all()]
        # admin_list = [group.name for group in groups]
        #
        # # 求交集
        # is_admin = [i for i in admin_list if i in admin_groups]
        # is_owner = [i for i in groups_list if i in admin_groups]
        #
        # if len(is_admin) > 0 or len(is_owner) > 0 or request.user == self.create_user:
        #     return True
        # else:
        #     return False
