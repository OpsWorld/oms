# -*- coding: utf-8 -*-
# author: itimor

from django.db import models
from hosts.models import Host

DEPLOY_STATUS = {
    "noaction": u"未执行",
    "deploy": u"发布中",
    "succed": u"发布成功",
    "failed": u"发布失败"
}


class Jobs(models.Model):
    name = models.CharField(max_length=20, unique=True, verbose_name=u'名称')
    hosts = models.ManyToManyField(Host, null=True, blank=True, verbose_name=u'被发布的主机')
    code_repo = models.CharField(u"代码仓库", max_length=30, default='svn')
    code_url = models.CharField(u"代码地址", max_length=100, null=True, blank=True)
    deploy_script = models.TextField(u'发布脚本', null=True, blank=True)
    deploy_status = models.CharField(u"发布状态", choices=DEPLOY_STATUS.items(), default="noaction", max_length=30)
    create_time = models.DateTimeField(u'创建时间', auto_now_add=True)
    update_time = models.DateTimeField(u'最近发布时间', auto_now=True)
    desc = models.CharField(u"描述", max_length=100, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u'项目或任务'
        verbose_name_plural = u'项目或任务'


class Deployenv(models.Model):
    job = models.ForeignKey(Jobs, verbose_name=u'发布任务')
    name = models.CharField(max_length=20, unique=True, verbose_name=u'名称')
    path = models.CharField(max_length=20, null=True, blank=True, verbose_name=u'发布路径')
    desc = models.CharField(u"描述", max_length=100, null=True, blank=True)


