# -*- coding: utf-8 -*-
# author: itimor

from rest_framework.decorators import api_view
from rest_framework.response import Response
from omsBackend.settings import sapi

@api_view()
def get_all_key(request):
    data = sapi.list_key()
    count = len(data)
    return Response({"results": data, "count": count})

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
def get_result(request,jid):
    data = sapi.get_result(jid)
    count = len(data)
    return Response({"results": data, "count": count})