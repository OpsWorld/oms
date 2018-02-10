# -*- coding: utf-8 -*-
# author: kiven

from django.db import models
from users.models import User, Group

Level = {
    1: 'A',
    2: 'B',
    3: 'C',
    4: 'D',
    5: 'E',
}

Status = {
    0: u'未指派',
    1: u'已指派',
    2: u'处理中',
    3: u'待审核',
    4: u'已解决',
}

admin_groups = ['admin', 'Tb_Development', 'OMS_Super_Admin']


class Project(models.Model):
    pid = models.BigIntegerField(unique=True, verbose_name=u'编号')
    title = models.CharField(max_length=100, blank=True, verbose_name=u'标题')
    type = models.ForeignKey('ProjectType', on_delete=models.SET_NULL, null=True, blank=True, verbose_name=u'类型')
    level = models.CharField(max_length=3, choices=Level.items(), default=2, verbose_name=u'等级')
    status = models.CharField(max_length=3, choices=Status.items(), default=0, verbose_name=u'状态')
    complete = models.IntegerField(default=0, blank=True, verbose_name=u'进度')
    content = models.TextField(verbose_name=u'内容')
    create_user = models.ForeignKey(User, related_name='project_create_user', verbose_name=u'创建者')
    action_user = models.ManyToManyField(User, null=True, blank=True, related_name='project_action_user', verbose_name=u'指派人')
    from_user = models.CharField(max_length=20, null=True, blank=True, verbose_name=u'需求人')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name=u'创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name=u'更新时间')
    start_time = models.DateTimeField(null=True, blank=True, verbose_name=u'开始时间')
    desc = models.TextField(null=True, blank=True, verbose_name=u'描述')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = u'项目'
        verbose_name_plural = u'项目'

    @staticmethod
    def has_read_permission(request):
        return True

    @staticmethod
    def has_object_read_permission(self, request):
        return True

    @staticmethod
    def has_write_permission(request):
        return True

    @staticmethod
    def has_object_write_permission(self, request):
        return True

    @staticmethod
    def has_update_permission(request):
        return True

    @staticmethod
    def has_object_update_permission(self, request):
        return True


class ProjectComment(models.Model):
    ticket = models.ForeignKey(Project, verbose_name=u'项目')
    content = models.TextField(verbose_name=u'回复内容')
    create_user = models.ForeignKey(User, verbose_name=u'回复人')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name=u'回复时间')

    class Meta:
        verbose_name = u'回复'
        verbose_name_plural = u'回复'


# class TicketEnclosure(models.Model):
#     ticket = models.ForeignKey(Project, verbose_name=u'工单')
#     file = models.ForeignKey(Upload, verbose_name=u'附件')
#     create_user = models.ForeignKey(User, verbose_name=u'附件上传人')
#     create_time = models.DateTimeField(auto_now_add=True, verbose_name=u'附件上传时间')
#
#     class Meta:
#         verbose_name = u'工单附件'
#         verbose_name_plural = u'工单附件'


class ProjectType(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name=u'项目类型')
    desc = models.TextField(null=True, blank=True, verbose_name=u'描述')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u'项目类型'
        verbose_name_plural = u'项目类型'
