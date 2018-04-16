# -*- coding: utf-8 -*-
# author: itimor

from rest_framework import viewsets
from rest_framework.response import Response
from dnsmanager.models import DnsApiKey, DnsDomain, DnsRecord
from dnsmanager.serializers import DnsApiKeySerializer, DnsDomainSerializer, DnsRecordSerializer
from dnsmanager.serializers import DnspodDomainSerializer, DnspodRecordSerializer, GodaddyDomainSerializer, \
    GodaddyRecordSerializer, BindDomainSerializer, BindRecordSerializer
from dnsmanager.dnspod_api import DnspodApi
from dnsmanager.godaddy_api import GodaddyApi
from dnsmanager.bind_api import BindApi


class DnsApiKeyViewSet(viewsets.ModelViewSet):
    queryset = DnsApiKey.objects.all()
    serializer_class = DnsApiKeySerializer
    filter_fields = ['name', 'type']
    search_fields = ['name']


class DnsDomainViewSet(viewsets.ModelViewSet):
    queryset = DnsDomain.objects.all().order_by('-update_time')
    serializer_class = DnsDomainSerializer
    filter_fields = ['name', 'type']
    search_fields = ['name']


class DnsRecordViewSet(viewsets.ModelViewSet):
    queryset = DnsRecord.objects.all()
    serializer_class = DnsRecordSerializer
    filter_fields = ['name', 'type', 'domain__name']
    search_fields = ['name']

    def create(self, request, *args, **kwargs):
        domain_type = request.data['domain_type']
        dnsinfo = DnsApiKey.objects.get(name=request.data['dnsname'])
        domain = request.data['domain']
        if domain_type == 'dnspod':
            dnsapi = DnspodApi(dnsinfo.key, dnsinfo.secret, '%s,%s' % (dnsinfo.key, dnsinfo.secret))
        elif domain_type == 'godaddy':
            dnsapi = GodaddyApi(dnsinfo.key, dnsinfo.secret)
        elif domain_type == 'bind':
            dnsapi = BindApi(user=dnsinfo.key, pwd=None, token=dnsinfo.secret)

        name = request.data['name']
        value = request.data['value']
        type = request.data['type']
        ttl = request.data['ttl']
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        query = dnsapi.add_record(domain, name, value, type, ttl)
        return Response(query)

    def update(self, request, *args, **kwargs):
        domain = request.data['domain']
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=False)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        domaininfo = DnsDomain.objects.get(name=domain)
        domain_type = domaininfo.type
        name = request.data['name']
        value = request.data['value']
        type = request.data['type']
        ttl = request.data['ttl']
        dnsinfo = DnsApiKey.objects.get(name=domaininfo.dnsname)
        if domain_type == 'dnspod':
            dnsapi = DnspodApi(dnsinfo.key, dnsinfo.secret, '%s,%s' % (dnsinfo.key, dnsinfo.secret))
            record_id = request.data['record_id']
            dnsapi.update_record(record_id, domain, name, value, type, ttl=ttl)
        elif domain_type == 'godaddy':
            dnsapi = GodaddyApi(dnsinfo.key, dnsinfo.secret)
            dnsapi.update_record(domain, name, value, type, ttl=ttl)
        elif domain_type == 'bind':
            dnsapi = BindApi(user=dnsinfo.key, pwd=None, token=dnsinfo.secret)
            record_id = request.data['record_id']
            dnsapi.update_record(record_id, domain, name, value, type, ttl=ttl)

        return Response(serializer.data)


class DnspodDomainViewSet(viewsets.ViewSet):
    serializer_class = DnspodDomainSerializer

    def list(self, request):
        dnsinfo = DnsApiKey.objects.get(name=request.GET['dnsname'])
        dnsapi = DnspodApi(dnsinfo.key, dnsinfo.secret, '%s,%s' % (dnsinfo.key, dnsinfo.secret))
        query = dnsapi.get_domains()
        serializer = DnspodDomainSerializer(query, many=True)
        return Response(serializer.data)

    def post(self, request):
        dnsinfo = DnsApiKey.objects.get(name=request.data['dnsname'])
        dnsapi = DnspodApi(dnsinfo.key, dnsinfo.secret, '%s,%s' % (dnsinfo.key, dnsinfo.secret))
        query = dnsapi.get_domains()
        for item in query:
            dnsdomain = dict()
            dnsdomain['dnsname'] = request.data['dnsname']
            dnsdomain['name'] = item['name']
            dnsdomain['type'] = 'dnspod'
            d, create = DnsDomain.objects.update_or_create(name=dnsdomain['name'], defaults=dnsdomain)
        return Response({'status': create})


class DnspodRecordViewSet(viewsets.ViewSet):
    serializer_class = DnspodRecordSerializer

    def list(self, request):
        dnsinfo = DnsApiKey.objects.get(name=request.GET['dnsname'])
        domain = request.GET['domain']
        dnsapi = DnspodApi(dnsinfo.key, dnsinfo.secret, '%s,%s' % (dnsinfo.key, dnsinfo.secret))
        query = dnsapi.get_records(domain)
        serializer = DnspodRecordSerializer(query, many=True)
        return Response(serializer.data)

    def post(self, request, record_type="A", ttl=600):
        dnsinfo = DnsApiKey.objects.get(name=request.data['dnsname'])
        domain = request.data['domain']
        dnsapi = DnspodApi(dnsinfo.key, dnsinfo.secret, '%s,%s' % (dnsinfo.key, dnsinfo.secret))
        if request.data['action'] == 'create':
            sub_domain = request.data['sub_domain']
            value = request.data['value']
            record_type = request.data.get('record_type', record_type)
            ttl = request.data.get('ttl', ttl)
            record = {
                'domain': DnsDomain.objects.get(name=domain),
                'name': sub_domain,
                'type': record_type,
                'value': value,
                'ttl': ttl,
            }
            DnsRecord.objects.update_or_create(**record)
            query = dnsapi.add_record(domain, sub_domain, value, record_type, ttl=ttl)
        elif request.data['action'] == 'update':
            sub_domain = request.data['sub_domain']
            value = request.data['value']
            record_type = request.data.get('record_type', record_type)
            ttl = request.data.get('ttl', ttl)
            record_id = request.data['record_id']
            record = {
                'value': value,
                'ttl': ttl,
            }
            domainquery = DnsDomain.objects.get(name=domain)
            DnsRecord.objects.update_or_create(domain=domainquery, name=sub_domain, type=record_type, **record)
            query = dnsapi.update_record(domain, record_id, sub_domain, value, record_type, ttl=ttl)
        elif request.data['action'] == 'remove':
            record_id = request.data['record_id']
            query = dnsapi.delete_record(domain, record_id)
        elif request.data['action'] == 'sync':
            query = dnsapi.get_records(domain)
            domainquery = DnsDomain.objects.get(name=domain)
            for item in query:
                dnsrecord = dict()
                dnsrecord['name'] = item['name']
                dnsrecord['type'] = item['type']
                dnsrecord['value'] = item['value']
                dnsrecord['ttl'] = item['ttl']
                dnsrecord['record_id'] = item['id']
                d, create = DnsRecord.objects.update_or_create(domain=domainquery, record_id=dnsrecord['record_id'],
                                                               defaults=dnsrecord)
            return Response({'status': create})
        return Response(query)


class GodaddyDomainViewSet(viewsets.ViewSet):
    serializer_class = GodaddyDomainSerializer

    def list(self, request):
        dnsinfo = DnsApiKey.objects.get(name=request.GET['dnsname'])
        dnsapi = GodaddyApi(dnsinfo.key, dnsinfo.secret)
        query = dnsapi.get_domains()
        serializer = GodaddyDomainSerializer(query, many=True)
        return Response(serializer.data)

    def post(self, request):
        dnsinfo = DnsApiKey.objects.get(name=request.data['dnsname'])
        dnsapi = GodaddyApi(dnsinfo.key, dnsinfo.secret)
        query = dnsapi.get_domains()
        for item in query:
            dnsdomain = dict()
            dnsdomain['dnsname'] = request.data['dnsname']
            dnsdomain['type'] = 'godaddy'
            dnsdomain['name'] = item['domain']
            d, create = DnsDomain.objects.update_or_create(name=dnsdomain['name'], defaults=dnsdomain)
        return Response({'status': create})


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
            record = {
                'domain': DnsDomain.objects.get(name=domain),
                'name': sub_domain,
                'type': record_type,
                'value': value,
                'ttl': ttl,
            }
            DnsRecord.objects.update_or_create(**record)
            query = dnsapi.add_record(domain, sub_domain, value, record_type, ttl=ttl)
        elif request.data['action'] == 'update':
            sub_domain = request.data['sub_domain']
            value = request.data['value']
            record_type = request.data.get('record_type', record_type)
            ttl = request.data.get('ttl', ttl)
            record = {
                'value': value,
                'ttl': ttl,
            }
            domainquery = DnsDomain.objects.get(name=domain)
            DnsRecord.objects.update_or_create(domain=domainquery, name=sub_domain, type=record_type, **record)
            query = dnsapi.update_record(domain, sub_domain, value, record_type, ttl=ttl)
        elif request.data['action'] == 'sync':
            query = dnsapi.get_records(domain)
            domainquery = DnsDomain.objects.get(name=domain)
            for item in query:
                dnsrecord = dict()
                dnsrecord['value'] = item['data']
                dnsrecord['ttl'] = item['ttl']
                d, create = DnsRecord.objects.update_or_create(domain=domainquery, name=item['name'], type=item['type'],
                                                               value=dnsrecord['value'], defaults=dnsrecord)
            return Response({'status': create})
        return Response(query)


class BindDomainViewSet(viewsets.ViewSet):
    serializer_class = BindDomainSerializer

    def list(self, request):
        dnsinfo = DnsApiKey.objects.get(name=request.GET['dnsname'])
        dnsapi = BindApi(user=dnsinfo.key, pwd=None, token=dnsinfo.secret)
        query = dnsapi.get_domains()
        serializer = BindDomainSerializer(query, many=True)
        return Response(serializer.data)

    def post(self, request):
        dnsinfo = DnsApiKey.objects.get(name=request.data['dnsname'])
        dnsapi = BindApi(user=dnsinfo.key, pwd=None, token=dnsinfo.secret)
        query = dnsapi.get_domains()
        for item in query:
            dnsdomain = dict()
            dnsdomain['dnsname'] = request.data['dnsname']
            dnsdomain['name'] = item['name']
            dnsdomain['type'] = 'bind'
            d, create = DnsDomain.objects.update_or_create(name=dnsdomain['name'], defaults=dnsdomain)
        return Response({'status': create})


class BindRecordViewSet(viewsets.ViewSet):
    serializer_class = BindRecordSerializer

    def list(self, request):
        dnsinfo = DnsApiKey.objects.get(name=request.GET['dnsname'])
        domain = request.GET['domain']
        dnsapi = BindApi(user=dnsinfo.key, pwd=None, token=dnsinfo.secret)
        query = dnsapi.get_records(domain)
        serializer = BindRecordSerializer(query, many=True)
        return Response(serializer.data)

    def post(self, request, record_type="A", ttl=600):
        dnsinfo = DnsApiKey.objects.get(name=request.data['dnsname'])
        domain = request.data['domain']
        dnsapi = BindApi(user=dnsinfo.key, pwd=None, token=dnsinfo.secret)
        if request.data['action'] == 'create':
            sub_domain = request.data['sub_domain']
            value = request.data['value']
            record_type = request.data.get('record_type', record_type)
            ttl = request.data.get('ttl', ttl)
            record = {
                'domain': DnsDomain.objects.get(name=domain),
                'name': sub_domain,
                'type': record_type,
                'value': value,
                'ttl': ttl,
            }
            DnsRecord.objects.update_or_create(**record)
            query = dnsapi.add_record(domain, sub_domain, value, record_type, ttl=ttl)
        elif request.data['action'] == 'update':
            sub_domain = request.data['sub_domain']
            value = request.data['value']
            record_type = request.data.get('record_type', record_type)
            ttl = request.data.get('ttl', ttl)
            record_id = request.data['record_id']
            record = {
                'value': value,
                'ttl': ttl,
            }
            domainquery = DnsDomain.objects.get(name=domain)
            DnsRecord.objects.update_or_create(domain=domainquery, name=sub_domain, type=record_type, **record)
            query = dnsapi.update_record(domain, record_id, sub_domain, value, record_type, ttl=ttl)
        elif request.data['action'] == 'sync':
            query = dnsapi.get_records(domain)
            domainquery = DnsDomain.objects.get(name=domain)
            for item in query:
                dnsrecord = dict()
                dnsrecord['name'] = item['name']
                dnsrecord['type'] = item['type']
                dnsrecord['value'] = item['value']
                dnsrecord['ttl'] = item['ttl']
                dnsrecord['record_id'] = item['id']
                d, create = DnsRecord.objects.update_or_create(domain=domainquery, record_id=dnsrecord['record_id'],
                                                               defaults=dnsrecord)
            return Response({'status': create})
        return Response(query)
