# -*- coding: utf-8 -*-
# author: kiven

from django.db import models
from users.models import User, Group
from tools.models import Upload

TicketStatus = {
    0: '进行中',
    1: '已完成',
    2: '搁置',
}


class OpsDemandManager(models.Model):
    pid = models.CharField(max_length=100, unique=True, verbose_name=u'编号')
    name = models.CharField(max_length=100, blank=True, verbose_name=u'标题')
    task_complete = models.IntegerField(default=0, blank=True, verbose_name=u'任务进度')
    content1 = models.TextField(verbose_name=u'目标')
    content2 = models.TextField(verbose_name=u'范围')
    content3 = models.TextField(verbose_name=u'预算')
    create_user = models.ForeignKey(User, related_name='optasks_demand_create_user', verbose_name=u'创建者')
    action_user = models.ManyToManyField(User, related_name='optasks_demand_action_user', verbose_name=u'参与者')
    status = models.CharField(max_length=3, choices=TicketStatus.items(), default=0, verbose_name=u'状态')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name=u'创建时间')
    start_time = models.DateField(verbose_name=u'开始时间')
    end_time = models.DateField(verbose_name=u'计划完成时间')
    desc = models.TextField(blank=True, null=True, verbose_name=u'备注')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u'项目'
        verbose_name_plural = u'项目'


class OpsDemandEnclosure(models.Model):
    project = models.ForeignKey(OpsDemandManager, verbose_name=u'项目')
    file = models.ForeignKey(Upload, verbose_name=u'附件')
    create_user = models.ForeignKey(User, verbose_name=u'附件上传人')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name=u'附件上传时间')

    class Meta:
        verbose_name = u'附件'
        verbose_name_plural = u'附件'


class OpsProject(models.Model):
    demand = models.ForeignKey(OpsDemandManager, verbose_name=u'需求')
    pid = models.CharField(max_length=100, unique=True, verbose_name=u'编号')
    name = models.CharField(max_length=100, blank=True, verbose_name=u'标题')
    task_complete = models.IntegerField(default=0, blank=True, verbose_name=u'任务进度')
    content1 = models.TextField(verbose_name=u'内容')
    content2 = models.TextField(verbose_name=u'完成情况')
    status = models.CharField(max_length=3, choices=TicketStatus.items(), default=0, verbose_name=u'状态')
    create_user = models.ForeignKey(User, related_name='optasks_create_user', verbose_name=u'创建者')
    action_user = models.ForeignKey(User, related_name='optasks_action_user', verbose_name=u'负责人')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name=u'创建时间')
    start_time = models.DateField(null=True, blank=True, verbose_name=u'开始时间')
    end_time = models.DateField(null=True, blank=True, verbose_name=u'计划完成时间')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u'项目'
        verbose_name_plural = u'项目'
