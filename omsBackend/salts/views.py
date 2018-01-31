# -*- coding: utf-8 -*-
# author: itimor

from rest_framework.decorators import api_view
from rest_framework.response import Response
from omsBackend.settings import sapi
from django.views.decorators.cache import cache_page
from hosts.models import Host
from records.models import Record


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
def sync_remote_server(request, method):
    tgt = '*'
    arg = ['osfinger', 'ipv4', 'cpu_model', 'num_cpus', 'memory_info', 'disk_info']
    data = sapi.sync_remote_server(tgt=tgt, arg=arg)
    count = len(data)
    for k, v in data.items():
        host_info = {
            'hostname': k,
            'os': v['osfinger'],
            'cpu': '{} * {}'.format(v['cpu_model'], v['num_cpus']),
            'memory': v['memory_info'],
            'disk': '|'.join(v['disk_info']),
            'ip': '|'.join(v['ipv4'])
        }

        if method == 'create':
            print("auto created start")
            try:
                obj = Host.objects.get(hostname=k)
            except Host.DoesNotExist:
                obj = Host(**host_info)
                obj.save()
                # records
                Record.objects.create(
                    name='hosts',
                    asset=k,
                    type=1,
                    method='create',
                    before='{}',
                    after=host_info,
                    create_user='auto'
                )
        else:
            print("auto updated start")
            host = Host.objects.update_or_create(
                hostname=k,
                defaults=host_info
            )
            # records
            Record.objects.create(
                name='hosts',
                asset=k,
                type=1,
                method='update',
                before='{}',
                after=host_info,
                create_user='auto'
            )

    return Response({"results": data, "count": count})
