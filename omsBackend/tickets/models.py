# -*- coding: utf-8 -*-
# author: kiven

from django.db import models
from users.models import User, Group
from tickets.storage import PathAndRename

TicketLevel = {
    1: 'A',
    2: 'B',
    3: 'C',
    4: 'D',
    5: 'E',
}

TicketStatus = {
    '0': u'未接收',
    '1': u'处理中',
    '2': u'未解决关闭问题',
    '3': u'已解决关闭问题',
}


class WorkTicket(models.Model):
    title = models.CharField(max_length=100, blank=True, verbose_name=u'工单标题')
    type = models.ForeignKey('TicketType', on_delete=models.SET_NULL, null=True, blank=True, verbose_name=u'工单类型')
    content = models.TextField(verbose_name=u'工单内容')
    create_user = models.ForeignKey(User, related_name='create_user', verbose_name=u'创建者')
    action_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='action_user',
                                    verbose_name=u'执行者')
    create_group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=u'所在部门')
    level = models.CharField(max_length=3, choices=TicketLevel.items(), default='5', verbose_name=u'工单等级')
    ticket_status = models.CharField(max_length=3, choices=TicketStatus.items(), default='0', verbose_name=u'工单状态')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name=u'工单创建时间')
    action_time = models.CharField(max_length=100, blank=True, verbose_name=u'工单接收时间')
    end_time = models.CharField(max_length=100, blank=True, verbose_name=u'工单结束时间')
    cost_time = models.CharField(max_length=20, blank=True, verbose_name=u'工单花费时间')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = u'工单'
        verbose_name_plural = u'工单'


class TicketComment(models.Model):
    ticket = models.ForeignKey(WorkTicket, verbose_name=u'工单')
    content = models.TextField(verbose_name=u'工单回复内容')
    create_user = models.ForeignKey(User, verbose_name=u'回复人')
    create_group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=u'所在部门')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name=u'工单回复时间')

    class Meta:
        verbose_name = u'工单回复'
        verbose_name_plural = u'工单回复'


path_and_rename = PathAndRename("./")


class TicketEnclosure(models.Model):
    ticket = models.ForeignKey(WorkTicket, verbose_name=u'工单')
    file = models.FileField(upload_to=path_and_rename, verbose_name=u'上传附件')
    create_user = models.ForeignKey(User, verbose_name=u'附件上传人')
    create_group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=u'所在部门')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name=u'附件上传时间')

    class Meta:
        verbose_name = u'工单附件'
        verbose_name_plural = u'工单附件'


class TicketType(models.Model):
    name = models.CharField(max_length=100, blank=True, verbose_name=u'工单类型')
    desc = models.TextField(null=True, blank=True, verbose_name=u'工单描述')

    class Meta:
        verbose_name = u'工单类型'
        verbose_name_plural = u'工单类型'


class TicketWiki(models.Model):
    title = models.CharField(max_length=100, blank=True, verbose_name=u'问题标题')
    type = models.CharField(max_length=100, null=True, blank=True, verbose_name=u'问题类型')
    content = models.TextField(verbose_name=u'问题内容')
    create_user = models.ForeignKey(User, verbose_name=u'创建者')
    create_group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=u'所在部门')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name=u'创建时间')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = u'问题wiki'
        verbose_name_plural = u'问题wiki'
