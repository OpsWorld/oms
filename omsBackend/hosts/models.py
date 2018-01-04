# -*- coding: utf-8 -*-
# author: itimor

from django.db import models

ASSET_STATUS = {
    'used': u'使用中',
    'noused': u'未使用',
    'broken': u'故障'
}

ASSET_TYPE = {
    'physical': u"物理机",
    'virtual': u"虚拟机",
    'container': u"容器",
    'network': u"网络设备",
    'other': u"其他设备"
}


class Host(models.Model):
    hostname = models.CharField(u"主机名", unique=True, max_length=50)
    ip = models.GenericIPAddressField(u"主IP", unique=True, max_length=15)
    other_ip = models.CharField(u"备用IP", max_length=100, null=True, blank=True)
    idc = models.ForeignKey('Idc', null=True, blank=True, verbose_name=u"机房")
    asset_type = models.CharField(u"设备类型", choices=ASSET_TYPE.items(), default='virtual', max_length=30)
    status = models.CharField(u"设备状态", choices=ASSET_STATUS.items(), default='used', max_length=30)
    os = models.CharField(u"操作系统", max_length=30, null=True, blank=True)
    cpu = models.CharField(u"CPU信息", max_length=30, null=True, blank=True)
    memory = models.CharField(u"内存信息", max_length=30, null=True, blank=True)
    disk = models.CharField(u"硬盘信息", max_length=30, null=True, blank=True)
    desc = models.TextField(u"备注", max_length=200, null=True, blank=True)

    def __str__(self):
        return self.hostname

    class Meta:
        verbose_name = u'服务器'
        verbose_name_plural = u'服务器'


class Idc(models.Model):
    name = models.CharField(u"名称", max_length=30, unique=True)
    user = models.CharField(u"联系人", max_length=30, null=True, blank=True)
    tel = models.CharField(u"联系人电话", max_length=30, null=True, blank=True)
    desc = models.CharField(u"描述", max_length=100, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u'idc'
        verbose_name_plural = u'idc'
