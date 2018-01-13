# -*- coding: utf-8 -*-
# author: kiven

from django.db import models
from users.models import User, Group
from tools.models import Upload

ChannelLevel = {
    1: 'A',
    2: 'B',
    3: 'C',
    4: 'D',
    5: 'E',
}

ChannelStatus = {
    0: u'未接收',
    1: u'正在处理',
    2: u'已解决',
}


class Platform(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name=u'平台名称')
    ipaddr = models.TextField(null=True, blank=True, verbose_name=u'ip地址')
    desc = models.TextField(null=True, blank=True, verbose_name=u'描述')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u'平台'
        verbose_name_plural = u'平台'


class Merchant(models.Model):
    platform = models.ForeignKey('Platform', verbose_name=u'依附平台')
    m_id = models.CharField(max_length=100, blank=True, verbose_name=u'商户名称')
    name = models.CharField(max_length=100, unique=True, verbose_name=u'商户号')
    domain = models.CharField(max_length=100, null=True, blank=True, verbose_name=u'绑定域名')
    three = models.CharField(max_length=100, null=True, blank=True, verbose_name=u'第三方业务经理')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u'商户'
        verbose_name_plural = u'商户'


class PayChannelName(models.Model):
    name = models.CharField(max_length=100, verbose_name=u'通道名称')
    desc = models.TextField(null=True, blank=True, verbose_name=u'描述')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u'支付通道类型'
        verbose_name_plural = u'支付通道类型'


class PayChannel(models.Model):
    platform = models.ForeignKey('Platform', verbose_name=u'依附平台')
    merchant = models.ForeignKey('Merchant', verbose_name=u'依附商户')
    type = models.ForeignKey('PayChannelName', verbose_name=u'通道类型')
    rate = models.CharField(max_length=10, blank=True, null=True, verbose_name=u'费率')
    keyinfo = models.TextField(max_length=500, blank=True, null=True, verbose_name=u'秘钥信息')
    m_forwardurl = models.CharField(max_length=100, blank=True, null=True, verbose_name=u'转发域名')
    m_submiturl = models.CharField(max_length=100, blank=True, null=True, verbose_name=u'提交域名')
    level = models.CharField(max_length=2, choices=ChannelLevel.items(), default=2, verbose_name=u'紧急度')
    status = models.CharField(max_length=3, choices=ChannelStatus.items(), default=0, null=True, blank=True,
                              verbose_name=u'状态')
    create_user = models.ForeignKey(User, related_name='pay_create_user', verbose_name=u'创建者')
    action_user = models.ForeignKey(User, related_name='pay_action_user', verbose_name=u'指派人')
    complete = models.IntegerField(default=0, blank=True, verbose_name=u'进度')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name=u'创建时间')

    class Meta:
        verbose_name = u'支付通道'
        verbose_name_plural = u'支付通道'


class ThreePayEnclosure(models.Model):
    ticket = models.ForeignKey('Platform', verbose_name=u'平台')
    file = models.ForeignKey(Upload, verbose_name=u'附件')
    create_user = models.ForeignKey(User, verbose_name=u'附件上传人')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name=u'附件上传时间')

    class Meta:
        verbose_name = u'通道附件'
        verbose_name_plural = u'通道附件'


class ThreePayComment(models.Model):
    ticket = models.ForeignKey(PayChannel, verbose_name=u'通道')
    merchant = models.ForeignKey('Merchant', verbose_name=u'依附商户')
    content = models.TextField(verbose_name=u'回复内容')
    create_user = models.ForeignKey(User, verbose_name=u'回复人')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name=u'回复时间')

    class Meta:
        verbose_name = u'通道测试'
        verbose_name_plural = u'通道测试'


class PlatformPayChannel(models.Model):
    name = models.CharField(max_length=100, unique=True, blank=True, verbose_name=u'名称')
    platform = models.ForeignKey('Platform', verbose_name=u'依附平台')
    type = models.ForeignKey('PayChannelName', verbose_name=u'通道类型')
    complete = models.IntegerField(default=0, blank=True, verbose_name=u'进度')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u'平台通道进度'
        verbose_name_plural = u'平台通道进度'

    def save(self, *args, **kwargs):
        if self.name == '':
            self.name = '{}-{}'.format(self.platform,self.type)
        super(PlatformPayChannel, self).save(*args, **kwargs)