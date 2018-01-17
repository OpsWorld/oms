# -*- coding: utf-8 -*-
# author: itimor

from rest_framework.decorators import api_view
from rest_framework.response import Response
from omsBackend.settings import sapi

@api_view()
def get_all_key(request):
    date = sapi.list_key()
    return Response({"results": date})

@api_view()
def minions_status(request):
    date = sapi.minions_status()
    return Response({"results": date})

@api_view()
def get_minion_info(request, key_id):
    date = sapi.get_minion_info(key_id)
    return Response({"results": date})