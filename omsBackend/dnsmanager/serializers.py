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
        fields = ['url', 'id', 'dnsname', 'name', 'status', 'type', 'create_time', 'expire_time', 'desc']


class DnsRecordSerializer(serializers.ModelSerializer):
    domain = serializers.SlugRelatedField(queryset=DnsDomain.objects.all(), slug_field='name')

    class Meta:
        model = DnsRecord
        fields = ['url', 'id', 'title', 'domain', 'name', 'status', 'type', 'value', 'ttl', 'use', 'desc']


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
    # expires = serializers.DateTimeField()
    createdAt = serializers.DateTimeField()


class GodaddyRecordSerializer(serializers.Serializer):
    name = serializers.CharField()
    data = serializers.CharField()
    type = serializers.CharField()
    ttl = serializers.IntegerField()
