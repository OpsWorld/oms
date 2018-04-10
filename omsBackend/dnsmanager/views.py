# -*- coding: utf-8 -*-
# author: itimor

from rest_framework import viewsets
from rest_framework.response import Response
from dnsmanager.models import DnsApiKey, DnsDomain, DnsRecord
from dnsmanager.serializers import DnsApiKeySerializer, DnsDomainSerializer, DnsRecordSerializer
from dnsmanager.serializers import DnspodDomainSerializer, DnspodRecordSerializer, GodaddyDomainSerializer, \
    GodaddyRecordSerializer
from dnsmanager.dnspod_api import DnspodApi
from dnsmanager.godaddy_api import GodaddyApi


class DnsApiKeyViewSet(viewsets.ModelViewSet):
    queryset = DnsApiKey.objects.all()
    serializer_class = DnsApiKeySerializer
    filter_fields = ['name', 'type']
    search_fields = ['name']


class DnsDomainViewSet(viewsets.ModelViewSet):
    queryset = DnsDomain.objects.all()
    serializer_class = DnsDomainSerializer
    filter_fields = ['name', 'type']
    search_fields = ['name']


class DnsRecordViewSet(viewsets.ModelViewSet):
    queryset = DnsRecord.objects.all()
    serializer_class = DnsRecordSerializer
    filter_fields = ['name', 'type']
    search_fields = ['name']


class DnspodDomainViewSet(viewsets.ViewSet):
    serializer_class = DnspodDomainSerializer

    def list(self, request):
        dnsinfo = DnsApiKey.objects.get(name=request.GET['dnsname'])
        dnsapi = DnspodApi(dnsinfo.key, dnsinfo.secret)
        query = dnsapi.get_domains()
        serializer = DnspodDomainSerializer(query, many=True)
        for item in query:
            dnsdomain = dict()
            if item['status'] == 'enable':
                dnsdomain['status'] = 0
            else:
                dnsdomain['status'] = 1
            dnsdomain['name'] = item['name']
            dnsdomain['type'] = 'dnspod'
            DnsDomain.objects.update_or_create(name=dnsdomain['name'], defaults=dnsdomain)
        return Response(serializer.data)


class DnspodRecordViewSet(viewsets.ViewSet):
    serializer_class = DnspodRecordSerializer

    def list(self, request):
        dnsinfo = DnsApiKey.objects.get(name=request.GET['dnsname'])
        domain = request.GET['domain']
        dnsapi = DnspodApi(dnsinfo.key, dnsinfo.secret)
        query = dnsapi.get_records(domain)
        serializer = DnspodRecordSerializer(query, many=True)
        return Response(serializer.data)

    def post(self, request, record_type="A", ttl=600):
        dnsinfo = DnsApiKey.objects.get(name=request.data['dnsname'])
        domain = request.data['domain']
        dnsapi = DnspodApi(dnsinfo.key, dnsinfo.secret)
        if request.data['action'] == 'create':
            sub_domain = request.data['sub_domain']
            value = request.data['value']
            record_type = request.data.get('record_type', record_type)
            ttl = request.data.get('ttl', ttl)
            query = dnsapi.add_record(domain, sub_domain, value, record_type, ttl=ttl)
        elif request.data['action'] == 'update':
            sub_domain = request.data['sub_domain']
            value = request.data['value']
            record_type = request.data.get('record_type', record_type)
            ttl = request.data.get('ttl', ttl)
            record_id = request.data['record_id']
            query = dnsapi.update_record(domain, record_id, sub_domain, value, record_type, ttl=ttl)
        elif request.data['action'] == 'remove':
            record_id = request.data['record_id']
            query = dnsapi.delete_record(domain, record_id)
        elif request.data['action'] == 'sync':
            query = dnsapi.get_records(domain)
            for item in query:
                dnsrecord = dict()
                if item['status'] == 'enabled':
                    dnsrecord['status'] = 0
                else:
                    dnsrecord['status'] = 1
                dnsrecord['dnsinfo'] = dnsinfo
                dnsrecord['domain'] = DnsDomain.objects.get(name=domain)
                dnsrecord['name'] = item['name']
                dnsrecord['value'] = item['value']
                dnsrecord['ttl'] = item['ttl']
                dnsrecord['type'] = item['type']
                d, create = DnsRecord.objects.update_or_create(dnsinfo=dnsrecord['dnsinfo'], name=dnsrecord['name'], defaults=dnsrecord)
                return create
        return Response(query)


class GodaddyDomainViewSet(viewsets.ViewSet):
    serializer_class = GodaddyDomainSerializer

    def list(self, request):
        dnsinfo = DnsApiKey.objects.get(name=request.GET['dnsname'])
        dnsapi = GodaddyApi(dnsinfo.key, dnsinfo.secret)
        query = dnsapi.get_domains()
        serializer = GodaddyDomainSerializer(query, many=True)
        for item in query:
            dnsdomain = dict()
            if item['status'] == 'ACTIVE':
                dnsdomain['status'] = 0
            else:
                dnsdomain['status'] = 1
            dnsdomain['type'] = 'godaddy'
            dnsdomain['name'] = item['domain']
            DnsDomain.objects.update_or_create(name=dnsdomain['name'], defaults=dnsdomain)
            return
        return Response(serializer.data)


class GodaddyRecordViewSet(viewsets.ViewSet):
    serializer_class = GodaddyRecordSerializer

    def list(self, request):
        dnsinfo = DnsApiKey.objects.get(name=request.GET['dnsname'])
        domain = request.GET['domain']
        dnsapi = GodaddyApi(dnsinfo.key, dnsinfo.secret)
        query = dnsapi.get_records(domain)
        serializer = GodaddyRecordSerializer(query, many=True)
        return Response(serializer.data)

    def post(self, request, record_type="A", ttl=600):
        dnsinfo = DnsApiKey.objects.get(name=request.data['dnsname'])
        domain = request.data['domain']
        dnsapi = GodaddyApi(dnsinfo.key, dnsinfo.secret)
        if request.data['action'] == 'create':
            sub_domain = request.data['sub_domain']
            value = request.data['value']
            record_type = request.data.get('record_type', record_type)
            ttl = request.data.get('ttl', ttl)
            query = dnsapi.add_record(domain, sub_domain, value, record_type, ttl=ttl)
        elif request.data['action'] == 'update':
            sub_domain = request.data['sub_domain']
            value = request.data['value']
            record_type = request.data.get('record_type', record_type)
            ttl = request.data.get('ttl', ttl)
            query = dnsapi.update_record(domain, sub_domain, value, record_type, ttl=ttl)
        return Response(query)
