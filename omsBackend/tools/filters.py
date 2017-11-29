# -*- coding: utf-8 -*-
# author: itimor

from django_filters import rest_framework as filters
from tools.models import Upload

class UploadFilter(filters.FilterSet):
    class Meta:
        model = Upload
        fields = {
            'id': ['exact'],
            'username': ['exact', 'contains'],
            'type': ['exact', 'contains'],
        }