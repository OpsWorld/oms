# -*- coding: utf-8 -*-
# author: itimor

from rest_framework import viewsets
from rest_framework.response import Response
from dnsmanager.models import DnsApiKey
from dnsmanager.serializers import DnsApiKeySerializer, DnspodDomainSerializer
from dnsmanager.dnspod_api import DnspodApi
from dnsmanager.dnspod_key import KEYINFO


class DnsApiKeyViewSet(viewsets.ModelViewSet):
    queryset = DnsApiKey.objects.all()
    serializer_class = DnsApiKeySerializer
    filter_fields = ['name']


class DnspodDomainViewSet(viewsets.ViewSet):
    serializer_class = DnspodDomainSerializer

    def list(self, request):
        dnsapi = DnspodApi(user=KEYINFO['user'], pwd=KEYINFO['pwd'])
        query = dnsapi.get_domains()
        serializer = DnspodDomainSerializer(query, many=True)
        return Response(serializer.data)
