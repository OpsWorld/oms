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
    0: '使用中',
    1: '备用',
    2: '被墙',
}


class DnsDomain(models.Model):
    dnsname = models.CharField(max_length=20, verbose_name=u'归属dns')
    name = models.CharField(max_length=20, unique=True, verbose_name=u'名称')
    status = models.CharField(choices=Dns_Status.items(), default=0, max_length=1, verbose_name=u'状态')
    type = models.CharField(choices=Dns_Types.items(), default='godaddy', max_length=10, verbose_name=u'类型')
    create_time = models.DateTimeField(null=True, blank=True, verbose_name=u'创建时间')
    expire_time = models.DateTimeField(null=True, blank=True, verbose_name=u'过期时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name=u'更新时间')
    desc = models.TextField(null=True, blank=True, verbose_name=u'备注')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        from utils.whois import whois
        domain_info = whois(self.name)
        self.create_time = domain_info["create_time"]
        self.expire_time = domain_info["expire_time"]
        super(DnsDomain, self).save(*args, **kwargs)


class DnsRecord(models.Model):
    domain = models.ForeignKey('DnsDomain', verbose_name=u'域名')
    title = models.CharField(max_length=200, unique=True, null=True, blank=True, verbose_name=u'标题')
    name = models.CharField(max_length=20, verbose_name=u'名称')
    status = models.CharField(choices=Dns_Status.items(), default=0, max_length=1, verbose_name=u'状态')
    type = models.CharField(default='A', max_length=10, verbose_name=u'类型')
    value = models.CharField(max_length=300, verbose_name=u'值')
    ttl = models.IntegerField(default=600, verbose_name=u'ttl')
    use = models.TextField(null=True, blank=True, verbose_name=u'用途')
    desc = models.TextField(null=True, blank=True, verbose_name=u'备注')

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.title = '{}-{}-{}-{}'.format(self.domain, self.name, self.type, self.value)
        super(DnsRecord, self).save(*args, **kwargs)
