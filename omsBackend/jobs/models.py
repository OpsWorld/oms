# -*- coding: utf-8 -*-
# author: itimor

from django.db import models
from hosts.models import Host
from users.models import User

DEPLOY_STATUS = {
    "deploy": "发布中",
    "success": "发布成功",
    "failed": "发布失败"
}

admin_groups = ['admin', 'OMS_Super_Admin']


class Jobs(models.Model):
    name = models.CharField(max_length=20, unique=True, verbose_name=u'名称')
    code_url = models.CharField(max_length=100, null=True, blank=True, verbose_name=u'代码地址')
    deploy_path = models.CharField(max_length=150, null=True, blank=True, verbose_name=u'发布路径')
    showdev = models.BooleanField(default=False, verbose_name=u'研发可见')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name=u'创建时间')
    desc = models.TextField(null=True, blank=True, verbose_name=u'描述')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u'项目或任务'
        verbose_name_plural = u'项目或任务'

    @staticmethod
    def has_read_permission(request):
        return True

    def has_object_read_permission(self, request):
        groups = User.objects.get(username=request.user).groups.all()
        admin_list = [group.name for group in groups]

        # 求交集
        is_admin = [i for i in admin_list if i in admin_groups]
        print(is_admin)
        if len(is_admin) > 0 or self.showdev:
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


class Deployenv(models.Model):
    job = models.ForeignKey(Jobs, verbose_name=u'发布任务')
    name = models.CharField(max_length=50, verbose_name=u'名称')
    deploy_hosts = models.ManyToManyField(Host, null=True, blank=True, verbose_name=u'发布主机')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u'发布环境'
        verbose_name_plural = u'发布环境'

    def save(self, *args, **kwargs):
        self.name = '{}-{}'.format(self.job, self.name)
        super(Deployenv, self).save(*args, **kwargs)


class Deploycmd(models.Model):
    env = models.ForeignKey(Deployenv, verbose_name=u'发布环境')
    name = models.CharField(max_length=10, verbose_name=u'名称')
    deploy_cmd = models.TextField(null=True, blank=True, verbose_name=u'发布命令')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u'发布命令'
        verbose_name_plural = u'发布命令'


class DeployJobs(models.Model):
    job = models.ForeignKey(Jobs, verbose_name=u'发布任务', related_name='deploy_job')
    j_id = models.CharField(max_length=50, null=True, blank=True, verbose_name=u'任务ID')
    deploy_status = models.CharField(choices=DEPLOY_STATUS.items(), default="deploy", max_length=30,
                                     verbose_name=u'发布状态')
    deploy_hosts = models.CharField(max_length=100, null=True, blank=True, verbose_name=u'发布主机')
    version = models.CharField(max_length=20, default='HEAD', verbose_name=u'版本号')
    content = models.TextField(verbose_name=u'更新内容')
    deploy_cmd = models.TextField( verbose_name=u'发布命令')
    action_user = models.ForeignKey(User, verbose_name=u'操作人')
    result = models.TextField(null=True, blank=True, verbose_name=u'发布结果')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name=u'创建时间')

    def __str__(self):
        return self.j_id

    class Meta:
        verbose_name = u'执行发布'
        verbose_name_plural = u'执行发布'
