# -*- coding: utf-8 -*-
# author: itimor

from django.db import models

Dns_Types = {
    'dnspod': 'dnspod',
    'godaddy': 'godaddy',
}


class DnsApiKey(models.Model):
    name = models.CharField(max_length=20, unique=True, verbose_name=u'名称')
    key = models.CharField(max_length=201, verbose_name=u'api_key')
    secret = models.CharField(max_length=201, verbose_name=u'api_secret')
    type = models.CharField(choices=Dns_Types.items(), default='godaddy', max_length=10, verbose_name=u'类型')
    desc = models.TextField(null=True, blank=True, verbose_name=u'备注')

    def __str__(self):
        return self.name


Dns_Status = {
    0: '启用',
    1: '停用',
}


class DnsDomain(models.Model):
    name = models.CharField(max_length=20, unique=True, verbose_name=u'名称')
    status = models.CharField(choices=Dns_Status.items(), default=0, max_length=1, verbose_name=u'状态')
    type = models.CharField(choices=Dns_Types.items(), default='godaddy', max_length=10, verbose_name=u'类型')
    desc = models.TextField(null=True, blank=True, verbose_name=u'备注')

    def __str__(self):
        return self.name


class DnsRecord(models.Model):
    domain = models.ForeignKey('DnsDomain', verbose_name=u'上级菜单')
    name = models.CharField(max_length=20, unique=True, verbose_name=u'名称')
    status = models.CharField(choices=Dns_Status.items(), default=0, max_length=1, verbose_name=u'状态')
    type = models.CharField(choices=Dns_Types.items(), default='godaddy', max_length=10, verbose_name=u'类型')
    value = models.CharField(max_length=101, verbose_name=u'值')
    ttl = models.IntegerField(default=600, verbose_name=u'ttl')
    desc = models.TextField(null=True, blank=True, verbose_name=u'备注')

    def __str__(self):
        return self.name
