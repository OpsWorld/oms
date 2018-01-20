# -*- coding: utf-8 -*-
# author: itimor

from rest_framework import serializers
from hosts.models import Host, Idc


class HostSerializer(serializers.ModelSerializer):
    idc = serializers.SlugRelatedField(queryset=Idc.objects.all(), slug_field='name')

    class Meta:
        model = Host
        fields = ['url', 'id', 'hostname', 'ip', 'other_ip', 'idc', 'asset_type', 'status', 'os', 'cpu',
                  'memory', 'disk', 'desc']


class IdcSerializer(serializers.ModelSerializer):
    class Meta:
        model = Idc
        fields = ['url', 'id', 'name', 'user', 'tel', 'desc']
