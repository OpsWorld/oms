# -*- coding: utf-8 -*-
# author: itimor

from rest_framework import viewsets
from hosts.models import Host, Idc
from hosts.serializers import HostSerializer, IdcSerializer
from rest_framework import status
from rest_framework.response import Response


class HostViewSet(viewsets.ModelViewSet):
    queryset = Host.objects.all()
    serializer_class = HostSerializer
    search_fields = ['hostname', 'ip']
    filter_fields = ['status']

    def partial_update(self, request, *args, **kwargs):
        serializer = HostSerializer(request.user, data=request.data, context={'request': request}, partial=True)
        print(request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class IdcViewSet(viewsets.ModelViewSet):
    queryset = Idc.objects.all()
    serializer_class = IdcSerializer
    filter_fields = ['name']


