# -*- coding: utf-8 -*-
# author: itimor

from rest_framework.decorators import api_view
from rest_framework.response import Response
from omsBackend.settings import sapi
from django.views.decorators.cache import cache_page
from hosts.models import Host
from records.models import Record
import json_tools
from utils.tools import removeNone


@api_view()
def get_all_key(request):
    data = sapi.list_key()
    count = len(data)
    return Response({"results": data, "count": count})


@cache_page(7200)
@api_view()
def minions_status(request):
    data = sapi.minions_status()
    up = data['up']
    down = data['down']
    ups = []
    downs = []
    for host in up:
        ups.append({'hostname': host, 'status': 'up'})
    for host in down:
        downs.append({'hostname': host, 'status': 'down'})
    data['up'] = ups
    data['down'] = downs
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
    data = sapi.remote_cmd(tgt=hosts, arg=cmd)
    count = len(data)
    return Response({"results": data, "count": count})


@api_view()
def get_result(request, jid):
    data = sapi.get_result(jid)
    count = len(data)
    return Response({"results": data, "count": count})


@api_view()
def sync_remote_server(request, method):
    tgt = sapi.minions_status()['up']
    arg = ['osfinger', 'ipv4', 'cpu_model', 'num_cpus', 'memory_info', 'disk_info']
    data = sapi.sync_remote_server(tgt=tgt, arg=arg)
    count = len(data)
    update_list = []
    no_update_list = []
    for k, v in data[0].items():
        host_info = {
            'hostname': k,
            'os': v['osfinger'],
            'cpu': '{} * {}'.format(v['cpu_model'], v['num_cpus']),
            'memory': v['memory_info'],
            'disk': '|'.join(v['disk_info']),
            'ip': '|'.join(v['ipv4'])
        }

        if method == 'create':
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
            try:
                obj = Host.objects.filter(hostname=k)
                obj_info = {
                    'hostname': k,
                    'os': obj[0].os,
                    'cpu': obj[0].cpu,
                    'memory': obj[0].memory,
                    'disk': obj[0].disk,
                    'ip': obj[0].ip
                }

                diff = removeNone(json_tools.diff(obj_info, host_info))
                if diff:
                    obj.update(**host_info)
                    # records
                    Record.objects.create(
                        name='hosts',
                        asset=k,
                        type=1,
                        method='update',
                        before=obj_info,
                        after=host_info,
                        diff=diff,
                        create_user='auto'
                    )
                    update_list.append(k)
                else:
                    no_update_list.append(k)

            except Host.DoesNotExist:
                print("%s is not exist" % k)
    print("update_list: %s" % update_list)
    print("no_update_list: %s" % no_update_list)

    return Response({"results": data, "count": count})
