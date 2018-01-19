# -*- coding: utf-8 -*-
# author: itimor

from django_filters import rest_framework as filters
from threepay.models import PlatformPayChannel

class PlatformPayChannelFilter(filters.FilterSet):
    class Meta:
        model = PlatformPayChannel
        fields = {
            'platform__name': ['exact'],
            'complete': ['gt', 'lt','exact'],
        }