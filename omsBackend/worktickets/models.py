# -*- coding: utf-8 -*-
# author: kiven

from django.db import models
from users.models import User, Group
from tools.models import Upload

TicketLevel = {
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


class WorkTicket(models.Model):
    ticketid = models.BigIntegerField(unique=True, verbose_name=u'工单编号')
    title = models.CharField(max_length=100, blank=True, verbose_name=u'工单标题')
    type = models.ForeignKey('TicketType', on_delete=models.SET_NULL, null=True, blank=True, verbose_name=u'工单类型')
    content = models.TextField(verbose_name=u'工单内容')
    create_user = models.ForeignKey(User, related_name='create_user', verbose_name=u'创建者')
    action_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='action_user',
                                    verbose_name=u'指派人')
    follower = models.ManyToManyField(User, null=True, blank=True, related_name='follower', verbose_name=u'跟踪人')
    create_group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=u'工单分组')
    level = models.CharField(max_length=3, choices=TicketLevel.items(), default=2, verbose_name=u'工单等级')
    ticket_status = models.CharField(max_length=3, choices=TicketStatus.items(), default=0, null=True, blank=True,
                                     verbose_name=u'工单状态')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name=u'工单创建时间')
    action_time = models.CharField(max_length=100, blank=True, verbose_name=u'工单接收时间')
    end_time = models.CharField(max_length=100, blank=True, verbose_name=u'工单结束时间')
    cost_time = models.CharField(max_length=20, blank=True, verbose_name=u'工单花费时间')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = u'工单'
        verbose_name_plural = u'工单'


class TicketComment(models.Model):
    ticket = models.ForeignKey(WorkTicket, verbose_name=u'工单')
    content = models.TextField(verbose_name=u'工单回复内容')
    create_user = models.ForeignKey(User, verbose_name=u'回复人')
    create_group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=u'所在部门')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name=u'工单回复时间')

    class Meta:
        verbose_name = u'工单回复'
        verbose_name_plural = u'工单回复'


class TicketEnclosure(models.Model):
    ticket = models.ForeignKey(WorkTicket, verbose_name=u'工单')
    file = models.ForeignKey(Upload, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=u'附件')
    create_user = models.ForeignKey(User, verbose_name=u'附件上传人')
    create_group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=u'所在部门')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name=u'附件上传时间')

    class Meta:
        verbose_name = u'工单附件'
        verbose_name_plural = u'工单附件'


class TicketType(models.Model):
    name = models.CharField(max_length=100, blank=True, verbose_name=u'工单类型')
    desc = models.TextField(null=True, blank=True, verbose_name=u'工单描述')

    class Meta:
        verbose_name = u'工单类型'
        verbose_name_plural = u'工单类型'


class TicketWiki(models.Model):
    title = models.CharField(max_length=100, blank=True, verbose_name=u'问题标题')
    type = models.CharField(max_length=100, null=True, blank=True, verbose_name=u'问题类型')
    content = models.TextField(verbose_name=u'问题内容')
    create_user = models.ForeignKey(User, verbose_name=u'创建者')
    create_group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=u'所在部门')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name=u'创建时间')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = u'问题wiki'
        verbose_name_plural = u'问题wiki'


# 商户开通通道
# 微信 网银 支付宝 银联快捷 快捷支付 QQ钱包 代付 H5微信 H5银联快捷 H5快捷支付 H5支付宝 京东钱包 银联扫码
# a b c d e f g h i j k l m
M_CHANNELS = {
    'a': u'微信',
    'b': u'网银',
    'c': u'支付宝',
    'd': u'银联快捷',
    'e': u'快捷支付',
    'f': u'QQ钱包',
    'g': u'代付',
    'h': u'H5微信',
    'i': u'H5银联快捷',
    'j': u'H5快捷支付',
    'k': u'H5支付宝',
    'l': u'京东钱包',
    'm': u'银联扫码',
}

PlatformStatus = {
    0: u'未接收',
    1: u'正在处理',
    2: u'已解决',
}


class ThreePayTicket(models.Model):
    ticketid = models.BigIntegerField(unique=True, verbose_name=u'工单编号')
    title = models.CharField(max_length=100, blank=True, verbose_name=u'工单标题')
    platform = models.CharField(max_length=100, blank=True, verbose_name=u'平台名称')
    level = models.CharField(max_length=3, choices=TicketLevel.items(), default=2, verbose_name=u'紧急度')
    status = models.CharField(max_length=3, choices=PlatformStatus.items(), default=0, null=True, blank=True,
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
    name = models.CharField(max_length=100, blank=True, verbose_name=u'平台名称')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u'平台'
        verbose_name_plural = u'平台'


class Merchant(models.Model):
    platform = models.ForeignKey(Platform, verbose_name=u'依附平台')
    name = models.CharField(max_length=100, blank=True, verbose_name=u'商户名称')
    m_backurl = models.CharField(max_length=100, blank=True, verbose_name=u'商户回调域名')
    m_id = models.CharField(max_length=100, blank=True, verbose_name=u'商户id')
    m_channel = models.CharField(max_length=100, blank=True, verbose_name=u'商户开通通道')
    m_md5key = models.CharField(max_length=100, blank=True, verbose_name=u'商户MD5KEY')
    m_public_key = models.CharField(max_length=500, blank=True, verbose_name=u'商户公钥')
    m_private_key = models.CharField(max_length=500, blank=True, verbose_name=u'商户私钥')
    p_public_key = models.CharField(max_length=500, blank=True, verbose_name=u'平台公钥')
    three = models.CharField(max_length=100, blank=True, verbose_name=u'第三方业务经理')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u'商户'
        verbose_name_plural = u'商户'


class PlatformEnclosure(models.Model):
    ticket = models.ForeignKey(ThreePayTicket, verbose_name=u'g')
    file = models.ForeignKey(Upload, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=u'附件')
    create_user = models.ForeignKey(User, verbose_name=u'附件上传人')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name=u'附件上传时间')

    class Meta:
        verbose_name = u'平台附件'
        verbose_name_plural = u'平台附件'
