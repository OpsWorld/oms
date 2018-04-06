# -*- coding: utf-8 -*-
# author: itimor

from rest_framework import viewsets
from rest_framework.response import Response
from dnsmanager.models import DnsApiKey
from dnsmanager.serializers import DnsApiKeySerializer, DnspodDomainSerializer, DnspodRecordSerializer
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


class DnspodRecordViewSet(viewsets.ViewSet):
    serializer_class = DnspodRecordSerializer

    def list(self, request):
        domain = request.GET['domain']
        dnsapi = DnspodApi(user=KEYINFO['user'], pwd=KEYINFO['pwd'])
        query = dnsapi.get_records(domain)
        serializer = DnspodRecordSerializer(query, many=True)
        return Response(serializer.data)

    def create(self, request, record_type="A", ttl=600):
        domain = request.data['domain']
        sub_domain = request.data['sub_domain']
        value = request.data['value']
        record_type = request.data.get('record_type', record_type)
        ttl = request.data.get('ttl', ttl)
        if not request.data['record_id']:
            dnsapi = DnspodApi(user=KEYINFO['user'], pwd=KEYINFO['pwd'])
            query = dnsapi.add_record(domain, sub_domain, value, record_type, ttl=ttl)
        else:
            record_id = request.data['record_id']
            dnsapi = DnspodApi(user=KEYINFO['user'], pwd=KEYINFO['pwd'])
            query = dnsapi.update_record(domain, record_id, sub_domain, value, record_type, ttl=ttl)
        return Response(query)