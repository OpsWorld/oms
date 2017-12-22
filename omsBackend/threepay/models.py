# -*- coding: utf-8 -*-
# author: kiven

from django.db import models
from users.models import User, Group
from tools.models import Upload

PayChannelLevel = {
    1: 'A',
    2: 'B',
    3: 'C',
    4: 'D',
    5: 'E',
}

TicketStatus = {
    0: u'未接收',
    1: u'正在处理',
    2: u'已解决',
}

class ThreePayTicket(models.Model):
    ticketid = models.BigIntegerField(unique=True, verbose_name=u'工单编号')
    title = models.CharField(max_length=100, blank=True, verbose_name=u'工单标题')
    platform = models.CharField(max_length=100, blank=True, verbose_name=u'平台名称')
    status = models.CharField(max_length=3, choices=TicketStatus.items(), default=0, null=True, blank=True,
                              verbose_name=u'工单状态')
    create_user = models.ForeignKey(User, related_name='three_create_user', verbose_name=u'创建者')
    action_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='three_action_user',
                                    verbose_name=u'指派人')
    follower = models.ManyToManyField(User, null=True, blank=True, related_name='three_follower', verbose_name=u'跟踪人')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name=u'工单创建时间')
    desc = models.TextField(null=True, blank=True, verbose_name=u'工单描述')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = u'第三支付工单'
        verbose_name_plural = u'第三支付工单'


class Platform(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name=u'平台名称')
    desc = models.TextField(null=True, blank=True, verbose_name=u'描述')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u'平台'
        verbose_name_plural = u'平台'


class Merchant(models.Model):
    platform = models.ForeignKey(Platform, verbose_name=u'依附平台')
    m_id = models.CharField(max_length=100, blank=True, verbose_name=u'商户号')
    name = models.CharField(max_length=100, unique=True, verbose_name=u'商户名称')
    three = models.CharField(max_length=100, blank=True, verbose_name=u'第三方业务经理')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u'商户'
        verbose_name_plural = u'商户'

class PayChannel(models.Model):
    merchant = models.ForeignKey(Merchant, verbose_name=u'依附商户')
    name = models.CharField(max_length=100, verbose_name=u'通道名称')
    m_md5key = models.CharField(max_length=100, blank=True, verbose_name=u'商户MD5KEY')
    m_public_key = models.CharField(max_length=500, blank=True, verbose_name=u'商户公钥')
    m_private_key = models.CharField(max_length=500, blank=True, verbose_name=u'商户私钥')
    p_public_key = models.CharField(max_length=500, blank=True, verbose_name=u'平台公钥')
    m_forwardurl = models.CharField(max_length=100, blank=True, verbose_name=u'商户转发域名')
    m_submiturl = models.CharField(max_length=100, blank=True, verbose_name=u'商户提交域名')
    m_backurl = models.CharField(max_length=100, blank=True, verbose_name=u'商户回调域名')
    level = models.CharField(max_length=3, choices=PayChannelLevel.items(), default=2, verbose_name=u'紧急度')

    def __str__(self):
        return '{}-{}'.format(self.merchant, self.name)

    class Meta:
        verbose_name = u'支付通道'
        verbose_name_plural = u'支付通道'


class PlatformEnclosure(models.Model):
    paychannel = models.ForeignKey(PayChannel, verbose_name=u'通道文档')
    file = models.ForeignKey(Upload, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=u'附件')
    create_user = models.ForeignKey(User, verbose_name=u'附件上传人')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name=u'附件上传时间')

    class Meta:
        verbose_name = u'通道附件'
        verbose_name_plural = u'通道附件'
