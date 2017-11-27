# -*- coding: utf-8 -*-
# author: itimor

from django_filters import rest_framework as filters
from tools.models import Duty, Upload

class DutyFilter(filters.FilterSet):
    class Meta:
        model = Duty
        fields = {
            'id': ['exact'],
            'username': ['exact', 'contains'],
            'shift': ['exact'],
            'create_time': ['exact', 'contains'],
        }

class UploadFilter(filters.FilterSet):
    class Meta:
        model = Upload
        fields = {
            'id': ['exact'],
            'username': ['exact', 'contains'],
            'type': ['exact', 'contains'],
        }