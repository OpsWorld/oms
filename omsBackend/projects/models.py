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
    0: u'未指派',
    1: u'已指派',
    2: u'处理中',
    3: u'待测试',
    4: u'测试中',
    5: u'已测试',
    6: u'待上线',
    7: u'已上线',
}

admin_groups = ['admin', 'Tb_Development', 'OMS_Super_Admin']
admin_users = ['admin', 'kiven', 'leon', 'omar', 'larry']


class Project(models.Model):
    pid = models.BigIntegerField(unique=True, verbose_name=u'编号')
    name = models.CharField(max_length=100, blank=True, verbose_name=u'标题')
    type = models.ForeignKey('ProjectType', on_delete=models.SET_NULL, null=True, blank=True, verbose_name=u'类型')
    level = models.CharField(max_length=3, choices=Level.items(), default=2, verbose_name=u'等级')
    status = models.CharField(max_length=3, choices=Project_Status.items(), default=0, verbose_name=u'状态')
    task_complete = models.IntegerField(default=0, blank=True, verbose_name=u'任务进度')
    test_complete = models.IntegerField(default=0, blank=True, verbose_name=u'测试进度')
    content = models.TextField(verbose_name=u'内容')
    create_user = models.ForeignKey(User, related_name='project_create_user', verbose_name=u'创建者')
    action_user = models.ManyToManyField(User, null=True, blank=True, related_name='project_action_user',
                                         verbose_name=u'指派人')
    follow_user = models.ManyToManyField(User, null=True, blank=True, related_name='project_follow_user',
                                         verbose_name=u'跟踪人')
    from_user = models.CharField(max_length=20, null=True, blank=True, verbose_name=u'需求人')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name=u'创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name=u'更新时间')
    start_time = models.DateField(null=True,blank=True, verbose_name=u'开始时间')
    end_time = models.DateField(null=True,blank=True, verbose_name=u'计划完成时间')
    is_public = models.BooleanField(default=True, verbose_name=u'是否公开')
    desc = models.TextField(null=True, blank=True, verbose_name=u'描述')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u'项目'
        verbose_name_plural = u'项目'


class ProjectComment(models.Model):
    project = models.ForeignKey(Project, verbose_name=u'项目')
    content = models.TextField(verbose_name=u'回复内容')
    create_user = models.ForeignKey(User, verbose_name=u'回复人')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name=u'回复时间')

    class Meta:
        verbose_name = u'回复'
        verbose_name_plural = u'回复'


class ProjectEnclosure(models.Model):
    project = models.ForeignKey(Project, verbose_name=u'项目')
    file = models.ForeignKey(Upload, verbose_name=u'附件')
    create_user = models.ForeignKey(User, verbose_name=u'附件上传人')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name=u'附件上传时间')

    class Meta:
        verbose_name = u'附件'
        verbose_name_plural = u'附件'


class ProjectType(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name=u'项目类型')
    desc = models.TextField(null=True, blank=True, verbose_name=u'描述')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u'项目类型'
        verbose_name_plural = u'项目类型'

TicketStatus = {
    0: u'未审核',
    1: u'已审核',
    2: u'未审核'
}


class Demand(models.Model):
    ticketid = models.BigIntegerField(unique=True, verbose_name=u'工单编号')
    title = models.CharField(max_length=100, blank=True, verbose_name=u'工单标题')
    type = models.ForeignKey('ProjectType', on_delete=models.SET_NULL, null=True, blank=True, verbose_name=u'工单类型')
    content = models.TextField(verbose_name=u'工单内容')
    create_user = models.ForeignKey(User, related_name='demand_create_user', verbose_name=u'创建者')
    action_user = models.ForeignKey(User, related_name='demand_action_user', verbose_name=u'操作人')
    ticket_status = models.CharField(max_length=3, choices=TicketStatus.items(), default=0, verbose_name=u'工单状态')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name=u'工单创建时间')
    end_time = models.DateField(null=True, blank=True, verbose_name=u'计划完成时间')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = u'需求'
        verbose_name_plural = u'需求'


Bug_Nice = {
    0: u'低',
    1: u'中',
    2: u'高'
}

Bug_Status = {
    0: u'新建',
    1: u'打开',
    2: u'关闭',
    3: u'已修复',
    4: u'暂不处理',
    5: u'重新打开'
}


class BugManager(models.Model):
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True, blank=True, related_name='bug_project', verbose_name=u'bug工单')
    test = models.ForeignKey('TestManager', related_name='test_bug', verbose_name=u'test')
    name = models.CharField(max_length=100, verbose_name=u'名称')
    desc = models.TextField(null=True, blank=True, verbose_name=u'描述')
    degree = models.CharField(max_length=3, choices=Level.items(), default=2, verbose_name=u'严重程度')
    nice = models.CharField(max_length=3, choices=Bug_Nice.items(), default=0, verbose_name=u'优先级')
    status = models.CharField(max_length=3, choices=Bug_Status.items(), default=0, verbose_name=u'状态')
    test_user = models.ForeignKey(User, related_name='bug_test_user', verbose_name=u'测试人员')
    action_user = models.ForeignKey(User, related_name='bug_action_user', verbose_name=u'分配给')
    test_time = models.DateField(blank=True, verbose_name=u'测试时间')
    end_time = models.DateField(null=True, blank=True, verbose_name=u'关闭时间')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u'bug管理'
        verbose_name_plural = u'bug管理'


Test_Status = {
    0: u'Passed',
    1: u'Failed',
    2: u'Block',
    3: u'N/A'
}


class TestManager(models.Model):
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True, blank=True, related_name='test_project', verbose_name=u'测试工单')
    name = models.CharField(max_length=100, verbose_name=u'名称')
    expect_result = models.TextField(null=True, blank=True, verbose_name=u'预期结果')
    actual_result = models.TextField(null=True, blank=True, verbose_name=u'实际结果')
    status = models.CharField(max_length=3, choices=Test_Status.items(), null=True, blank=True, verbose_name=u'执行状态')
    test_user = models.ForeignKey(User, related_name='test_test_user', verbose_name=u'测试人员')
    action_user = models.ForeignKey(User, related_name='test_action_user', verbose_name=u'开发人员')
    test_time = models.DateField(blank=True, verbose_name=u'测试时间')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u'测试管理'
        verbose_name_plural = u'测试管理'
