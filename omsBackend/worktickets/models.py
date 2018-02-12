# -*- coding: utf-8 -*-
# author: kiven

from django.db import models
from users.models import User, Group
from tools.models import Upload


TicketLevel = {
    1: 'A',
    2: 'B',
    3: 'C',
    4: 'D',
    5: 'E',
}

TicketStatus = {
    0: u'未接收',
    1: u'正在处理',
    2: u'已解决',
}

admin_groups = ['admin', 'Tb_Development', 'OMS_Super_Admin']


class WorkTicket(models.Model):
    ticketid = models.BigIntegerField(unique=True, verbose_name=u'工单编号')
    title = models.CharField(max_length=100, blank=True, verbose_name=u'工单标题')
    type = models.ForeignKey('TicketType', on_delete=models.SET_NULL, null=True, blank=True, verbose_name=u'工单类型')
    content = models.TextField(verbose_name=u'工单内容')
    create_user = models.ForeignKey(User, related_name='create_user', verbose_name=u'创建者')
    action_user = models.ForeignKey(User, related_name='action_user', verbose_name=u'指派人')
    edit_user = models.ForeignKey(User, related_name='edit_user', blank=True, null=True, verbose_name=u'处理人')
    create_group = models.ManyToManyField(Group, null=True, blank=True, verbose_name=u'部门')
    level = models.CharField(max_length=3, choices=TicketLevel.items(), default=2, verbose_name=u'工单等级')
    ticket_status = models.CharField(max_length=3, choices=TicketStatus.items(), default=0, verbose_name=u'工单状态')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name=u'工单创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name=u'工单更新时间')
    action_time = models.CharField(max_length=100, blank=True, verbose_name=u'工单接收时间')
    end_time = models.CharField(max_length=100, blank=True, verbose_name=u'工单结束时间')
    cost_time = models.CharField(max_length=20, blank=True, verbose_name=u'工单花费时间')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = u'工单'
        verbose_name_plural = u'工单'

    @staticmethod
    def has_read_permission(request):
        return True

    def has_object_read_permission(self, request):
        groups = User.objects.get(username=request.user).groups.all()
        create_groups = self.create_group.all()
        admin_list = [group.name for group in groups]

        # 求交集
        is_admin = [i for i in admin_list if i in admin_groups]
        c_list = groups & create_groups
        print(is_admin)
        if len(is_admin) > 0 or len(c_list) > 0:
            return True
        else:
            return False

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


class TicketComment(models.Model):
    ticket = models.ForeignKey(WorkTicket, verbose_name=u'工单')
    content = models.TextField(verbose_name=u'工单回复内容')
    create_user = models.ForeignKey(User, verbose_name=u'回复人')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name=u'工单回复时间')

    class Meta:
        verbose_name = u'工单回复'
        verbose_name_plural = u'工单回复'


class TicketEnclosure(models.Model):
    ticket = models.ForeignKey(WorkTicket, verbose_name=u'工单')
    file = models.ForeignKey(Upload, verbose_name=u'附件')
    create_user = models.ForeignKey(User, verbose_name=u'附件上传人')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name=u'附件上传时间')

    class Meta:
        verbose_name = u'工单附件'
        verbose_name_plural = u'工单附件'


class TicketType(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name=u'工单类型')
    desc = models.TextField(null=True, blank=True, verbose_name=u'描述')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u'工单类型'
        verbose_name_plural = u'工单类型'