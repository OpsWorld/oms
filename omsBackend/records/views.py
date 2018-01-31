# -*- coding: utf-8 -*-
# author: itimor

from rest_framework import viewsets
from records.models import Record
from records.serializers import RecordSerializer
from records.filters import RecordFilter


class RecordViewSet(viewsets.ModelViewSet):
    queryset = Record.objects.all().order_by('-create_time')
    serializer_class = RecordSerializer
    filter_class = RecordFilter
    search_fields = ['asset']

