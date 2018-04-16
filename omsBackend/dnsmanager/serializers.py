# -*- coding: utf-8 -*-
# author: itimor

from rest_framework import serializers
from dnsmanager.models import DnsApiKey, DnsDomain, DnsRecord


class DnsApiKeySerializer(serializers.ModelSerializer):
    class Meta:
        model = DnsApiKey
        fields = ['url', 'id', 'name', 'key', 'secret', 'type', 'desc']


class DnsDomainSerializer(serializers.ModelSerializer):
    class Meta:
        model = DnsDomain
        fields = ['url', 'id', 'title', 'dnsname', 'name', 'dnsService', 'status', 'type', 'create_time', 'expire_time',
                  'update_time', 'desc']


class DnsRecordSerializer(serializers.ModelSerializer):
    domain = serializers.SlugRelatedField(queryset=DnsDomain.objects.all(), slug_field='name')

    class Meta:
        model = DnsRecord
        fields = ['url', 'id', 'title', 'domain', 'name', 'status', 'type', 'value', 'ttl', 'record_id', 'use', 'desc']


class DnspodDomainSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    status = serializers.CharField()
    records = serializers.CharField()
    created_on = serializers.DateTimeField()


class DnspodRecordSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    line = serializers.CharField()
    type = serializers.CharField()
    ttl = serializers.CharField()
    value = serializers.CharField()
    mx = serializers.CharField()
    status = serializers.CharField()
    updated_on = serializers.DateTimeField()


class GodaddyDomainSerializer(serializers.Serializer):
    domainId = serializers.IntegerField()
    domain = serializers.CharField()
    status = serializers.CharField()
    createdAt = serializers.DateTimeField()


class GodaddyRecordSerializer(serializers.Serializer):
    name = serializers.CharField()
    data = serializers.CharField()
    type = serializers.CharField()
    ttl = serializers.IntegerField()


class BindDomainSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()


class BindRecordSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    type = serializers.CharField()
    value = serializers.CharField()
    ttl = serializers.CharField()
    mx = serializers.CharField()
    domain_id = serializers.IntegerField()
    expire = serializers.IntegerField()
    minimum = serializers.IntegerField()
    refresh = serializers.IntegerField()
    retry = serializers.IntegerField()
    serial = serializers.IntegerField()
