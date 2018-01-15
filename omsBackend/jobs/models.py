# -*- coding: utf-8 -*-
# author: itimor

from django.db import models
from hosts.models import Host
from users.models import User

DEPLOY_STATUS = {
    "deploy": u"发布中",
    "success": u"发布成功",
    "failed": u"发布失败"
}


class Jobs(models.Model):
    name = models.CharField(max_length=20, unique=True, verbose_name=u'名称')
    code_repo = models.CharField(max_length=30, default='svn', verbose_name=u'代码仓库')
    code_url = models.CharField(max_length=100, null=True, blank=True, verbose_name=u'代码地址')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name=u'创建时间')
    desc = models.TextField(null=True, blank=True, verbose_name=u'描述')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u'项目或任务'
        verbose_name_plural = u'项目或任务'


class Deployenv(models.Model):
    job = models.ForeignKey(Jobs, verbose_name=u'发布任务')
    name = models.CharField(max_length=20, verbose_name=u'名称')
    hosts = models.ManyToManyField(Host, null=True, blank=True, verbose_name=u'发布主机')
    path = models.CharField(max_length=20, null=True, blank=True, verbose_name=u'发布路径')
    desc = models.TextField(null=True, blank=True, verbose_name=u'描述')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u'发布环境'
        verbose_name_plural = u'发布环境'


class DeployJobs(models.Model):
    job = models.ForeignKey(Jobs, verbose_name=u'发布任务')
    j_id = models.CharField(max_length=50, null=True, blank=True, verbose_name=u'任务ID')
    deploy_status = models.CharField(choices=DEPLOY_STATUS.items(), default="deploy", max_length=30,verbose_name=u'发布状态')
    hosts = models.CharField(max_length=20, null=True, blank=True, verbose_name=u'发布主机')
    env = models.CharField(max_length=20, null=True, blank=True, verbose_name=u'发布环境')
    version = models.CharField(max_length=20, default='HEAD', verbose_name=u'版本号')
    deploy_path = models.CharField(max_length=20, null=True, blank=True, verbose_name=u'发布路径')
    action_user = models.ForeignKey(User, verbose_name=u'操作人')
    result = models.TextField(null=True, blank=True, verbose_name=u'发布结果')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name=u'创建时间')


    def __str__(self):
        return self.j_id

    class Meta:
        verbose_name = u'执行发布'
        verbose_name_plural = u'执行发布'
