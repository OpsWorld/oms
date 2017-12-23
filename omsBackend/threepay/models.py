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
    desc = models.TextField(null=True, blank=True, verbose_name=u'描述')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u'平台'
        verbose_name_plural = u'平台'


class Merchant(models.Model):
    platform = models.ForeignKey('Platform', verbose_name=u'依附平台')
    m_id = models.CharField(max_length=100, blank=True, verbose_name=u'商户号')
    name = models.CharField(max_length=100, unique=True, verbose_name=u'商户名称')
    three = models.CharField(max_length=100, blank=True, verbose_name=u'第三方业务经理')

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
    m_md5key = models.CharField(max_length=100, blank=True, verbose_name=u'商户MD5KEY')
    m_public_key = models.CharField(max_length=500, blank=True, verbose_name=u'商户公钥')
    m_private_key = models.CharField(max_length=500, blank=True, verbose_name=u'商户私钥')
    p_public_key = models.CharField(max_length=500, blank=True, verbose_name=u'平台公钥')
    m_forwardurl = models.CharField(max_length=100, blank=True, verbose_name=u'转发域名')
    m_submiturl = models.CharField(max_length=100, blank=True, verbose_name=u'提交域名')
    m_backurl = models.CharField(max_length=100, blank=True, verbose_name=u'回调域名')
    level = models.CharField(max_length=2, choices=ChannelLevel.items(), default=2, verbose_name=u'紧急度')
    status = models.CharField(max_length=3, choices=ChannelStatus.items(), default=0, null=True, blank=True,verbose_name=u'状态')
    action_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=u'指派人')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name=u'创建时间')

    class Meta:
        verbose_name = u'支付通道'
        verbose_name_plural = u'支付通道'


class ThreePayEnclosure(models.Model):
    ticket = models.ForeignKey('PayChannel', verbose_name=u'通道')
    file = models.ForeignKey(Upload, verbose_name=u'附件')
    create_user = models.ForeignKey(User, verbose_name=u'附件上传人')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name=u'附件上传时间')

    class Meta:
        verbose_name = u'通道附件'
        verbose_name_plural = u'通道附件'
