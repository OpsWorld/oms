# -*- coding: utf-8 -*-
# author: kiven

from rest_framework import viewsets
from zkmanager.models import ZkUser, Punch, PunchSet
from zkmanager.serializers import ZkUserSerializer, PunchSerializer, PunchSetSerializer
from zkmanager.filters import PunchFilter


class ZkUserViewSet(viewsets.ModelViewSet):
    queryset = ZkUser.objects.all()
    serializer_class = ZkUserSerializer
    search_fields = ['user_id', 'username']


class PunchViewSet(viewsets.ModelViewSet):
    queryset = Punch.objects.all().order_by('user_id', 'create_date')
    serializer_class = PunchSerializer
    filter_class = PunchFilter
    search_fields = ['user__username']


class PunchSetViewSet(viewsets.ModelViewSet):
    queryset = PunchSet.objects.all()
    serializer_class = PunchSetSerializer

