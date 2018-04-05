# -*- coding: utf-8 -*-
# author: itimor

from rest_framework import serializers
from dnsmanager.models import DnsApiKey


class DnsApiKeySerializer(serializers.ModelSerializer):
    class Meta:
        model = DnsApiKey
        fields = ['url', 'id', 'name', 'key', 'secret', 'type', 'desc']
