# -*- coding: utf-8 -*-
# author: itimor

from django.db import models
from tools.filesize import convert_size
from tools.storage import PathAndRename
import os
from users.models import User

class Upload(models.Model):
    username = models.CharField(max_length=20, verbose_name=u'上传用户')
    file = models.FileField(upload_to=PathAndRename("./"), blank=True, verbose_name=u'上传文件')
    archive = models.CharField(max_length=101, default=u'其他', null=True, blank=True, verbose_name=u'文件归档')
    filename = models.CharField(max_length=201, null=True, blank=True, verbose_name=u'文件名')
    filepath = models.CharField(max_length=201, null=True, blank=True, verbose_name=u'文件路径')
    type = models.CharField(max_length=20, null=True, blank=True, verbose_name=u'文件类型')
    size = models.CharField(max_length=20, null=True, blank=True, verbose_name=u'文件大小')
    create_time = models.CharField(max_length=20, null=True, blank=True, verbose_name=u'文件日期')

    def save(self, *args, **kwargs):
        self.size = '{}'.format(convert_size(self.file.size))
        filename = os.path.splitext(self.file.name)
        self.filename = '{}-{}{}'.format(filename[0], self.create_time, filename[1])
        self.filepath = '{}/{}'.format(self.archive, self.filename)
        super(Upload, self).save(*args, **kwargs)

    def __str__(self):
        return self.filepath

    class Meta:
        verbose_name = u'文件上传'
        verbose_name_plural = u'文件上传'

class Sendmail(models.Model):
    to = models.CharField(max_length=30, verbose_name=u'收件人')
    cc = models.CharField(max_length=100, null=True, blank=True, verbose_name=u'抄送人')
    sub = models.CharField(max_length=101, default=u'其他', verbose_name=u'邮件主题')
    content = models.TextField(null=True, blank=True, verbose_name=u'邮件内容')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name=u'邮件创建时间')

    class Meta:
        verbose_name = u'发送邮件'
        verbose_name_plural = u'发送邮件'


class Sendmessage(models.Model):
    action_user = models.CharField(max_length=100, verbose_name=u'收件人')
    title = models.CharField(max_length=30, verbose_name=u'消息标题')
    message = models.TextField(null=True, blank=True, verbose_name=u'消息')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = u'发送消息提醒'
        verbose_name_plural = u'发送消息提醒'

class SaltApi(models.Model):
    name = models.CharField(u"名称", max_length=30, unique=True)
    apiaddr = models.URLField(max_length=20, verbose_name=u'saltAPI地址')
    username = models.CharField(max_length=20, verbose_name=u'用户名')
    password = models.CharField(max_length=30, verbose_name=u'密码')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u'saltAPI地址'
        verbose_name_plural = u'saltAPI地址'