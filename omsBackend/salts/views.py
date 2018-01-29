# -*- coding: utf-8 -*-
# author: itimor

from rest_framework.decorators import api_view
from rest_framework.response import Response
from omsBackend.settings import sapi
from django.views.decorators.cache import cache_page
from hosts.models import Host


@api_view()
def get_all_key(request):
    data = sapi.list_key()
    count = len(data)
    return Response({"results": data, "count": count})


@cache_page(86400)
@api_view()
def minions_status(request):
    data = sapi.minions_status()
    return Response({"results": data})


@api_view()
def get_minion_info(request, key_id):
    data = sapi.get_minion_info(key_id)
    count = len(data)
    return Response({"results": data, "count": count})


@api_view(['POST'])
def cmdrun(request):
    hosts = request.data["hosts"]
    cmd = request.data["cmd"]
    data = sapi.remote_cmd(tgt=hosts, fun='cmd.run', arg=cmd)
    count = len(data)
    return Response({"results": data, "count": count})


@api_view()
def get_result(request, jid):
    data = sapi.get_result(jid)
    count = len(data)
    return Response({"results": data, "count": count})


@api_view()
def sync_remote_server(request):
    tgt = '*'
    arg = ['osfinger', 'ipv4', 'cpu_model', 'memory_info', 'disk_info']
    data = sapi.sync_remote_server(tgt=tgt, arg=arg)
    count = len(data)
    for k, v in data.items():
        addhost, created = Host.objects.update_or_create(
            hostname=k,
            os=v['osfinger'],
            cpu=v['cpu_model'],
            memory=v['memory_info'],
            disk='|'.join(v['disk_info']),
            ip='|'.join(v['ipv4'])
        )
        if created:
            print('%s add succed' % k)
    return Response({"results": data, "count": count})
