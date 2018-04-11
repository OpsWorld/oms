# -*- coding: utf-8 -*-
# author: itimor

from django.db import models
from django.utils import timezone


class ZkUser(models.Model):
    user_id = models.IntegerField(primary_key=True, unique=True, verbose_name=u"用户号")
    username = models.CharField(max_length=30, verbose_name=u"用户名")
    password = models.CharField(max_length=30, null=True, blank=True, verbose_name=u"密码")
    role = models.CharField(max_length=30, default=0, verbose_name=u"身份")
    is_active = models.BooleanField(verbose_name=u"启用")

    def __str__(self):
        return self.username


SworkStatus = {
    0: '已签到',
    1: '迟到',
    2: '未签到'
}

EworkStatus = {
    0: '已签退',
    1: '早退',
    2: '未签退',
}


class Punch(models.Model):
    user = models.ForeignKey('ZkUser', on_delete=models.SET_NULL, null=True, blank=True, verbose_name=u"用户")
    verifymode = models.CharField(max_length=30, default=1, verbose_name=u"打卡模式")
    swork_status = models.CharField(max_length=3, choices=SworkStatus.items(), default=2, verbose_name=u'签到状态')
    ework_status = models.CharField(max_length=3, choices=EworkStatus.items(), default=2, verbose_name=u'签退状态')
    nowork_status = models.BooleanField(default=False, verbose_name=u'旷工状态')
    create_date = models.DateField(default=timezone.now, verbose_name=u'打卡日期')
    swork_time = models.TimeField(null=True, blank=True, verbose_name=u'签到时间')
    ework_time = models.TimeField(null=True, blank=True, verbose_name=u'签退时间')
    swork_timec = models.TimeField(null=True, blank=True, verbose_name=u'迟到时间')
    ework_timec = models.TimeField(null=True, blank=True, verbose_name=u'早退时间')
    work_time = models.TimeField(null=True, blank=True, verbose_name=u'实际工作时间')


class PunchSet(models.Model):
    swork_time = models.TimeField(default=timezone.now, verbose_name=u'上班时间')
    ework_time = models.TimeField(default=timezone.now, verbose_name=u'下班时间')
    swork_stime = models.TimeField(default=timezone.now, verbose_name=u'上班打卡开始时间')
    swork_etime = models.TimeField(default=timezone.now, verbose_name=u'上班打卡结束时间')
    ework_stime = models.TimeField(default=timezone.now, verbose_name=u'下班打卡开始时间')
    ework_etime = models.TimeField(default=timezone.now, verbose_name=u'下班打卡结束时间')
    timeout = models.CharField(max_length=30, default=0, verbose_name=u"允许超时分钟")
