# -*- coding: utf-8 -*-
# author: kiven

from django.db import models
from users.models import User, Group
from tools.models import Upload

Level = {
    1: 'A',
    2: 'B',
    3: 'C',
    4: 'D',
    5: 'E',
}

Project_Status = {
    0: '未处理',
    1: '处理中',
    2: '已上线',
}


class Project(models.Model):
    pid = models.CharField(max_length=100, unique=True, verbose_name=u'编号')
    name = models.CharField(max_length=100, blank=True, verbose_name=u'标题')
    type = models.ForeignKey('ProjectType', on_delete=models.SET_NULL, null=True, blank=True, verbose_name=u'类型')
    level = models.CharField(max_length=3, choices=Level.items(), default=2, verbose_name=u'等级')
    status = models.CharField(max_length=3, choices=Project_Status.items(), default=0, verbose_name=u'状态')
    task_complete = models.IntegerField(default=0, blank=True, verbose_name=u'任务进度')
    content = models.TextField(verbose_name=u'内容')
    create_user = models.ForeignKey(User, related_name='optasks_create_user', verbose_name=u'创建者')
    action_user = models.ForeignKey(User, related_name='optasks_action_user', verbose_name=u'指派人')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name=u'创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name=u'更新时间')
    start_time = models.DateField(null=True, blank=True, verbose_name=u'开始时间')
    end_time = models.DateField(null=True, blank=True, verbose_name=u'计划完成时间')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u'项目'
        verbose_name_plural = u'项目'


class ProjectType(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name=u'项目类型')
    desc = models.TextField(null=True, blank=True, verbose_name=u'描述')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u'项目类型'
        verbose_name_plural = u'项目类型'


class ProjectEnclosure(models.Model):
    project = models.ForeignKey(Project, verbose_name=u'项目')
    file = models.ForeignKey(Upload, related_name='optask_enclosure_file', verbose_name=u'附件')
    create_user = models.ForeignKey(User, related_name='optask_enclosure_create_user', verbose_name=u'附件上传人')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name=u'附件上传时间')

    class Meta:
        verbose_name = u'附件'
        verbose_name_plural = u'附件'


TicketStatus = {
    0: '未审核',
    1: '已通过',
    2: '未通过'
}


class DemandManager(models.Model):
    pid = models.CharField(max_length=100, unique=True, verbose_name=u'工单编号')
    name = models.CharField(max_length=100, blank=True, verbose_name=u'工单标题')
    type = models.ForeignKey('ProjectType', on_delete=models.SET_NULL, null=True, blank=True, verbose_name=u'工单类型')
    content = models.TextField(verbose_name=u'工单内容')
    create_user = models.ForeignKey(User, related_name='optasks_demand_create_user', verbose_name=u'创建者')
    status = models.CharField(max_length=3, choices=TicketStatus.items(), default=0, verbose_name=u'工单状态')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name=u'工单创建时间')
    end_time = models.DateField(null=True, blank=True, verbose_name=u'计划完成时间')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u'需求'
        verbose_name_plural = u'需求'