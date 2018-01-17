# -*- coding: utf-8 -*-
# author: itimor

from rest_framework.decorators import api_view
from rest_framework.response import Response
from omsBackend.settings import sapi

@api_view()
def get_all_key(request):
    date = sapi.list_key()
    return Response({"data": date})

@api_view()
def accept_key(request, key_id):
    date = sapi.accept_key(key_id)
    return Response({"data": date})

@api_view()
def delete_key(request, key_id):
    date = sapi.delete_key(key_id)
    return Response({"data": date})

@api_view()
def minions_status(request):
    date = sapi.minions_status()
    return Response({"data": date})