# -*- coding: utf-8 -*-
# author: itimor

from rest_framework import viewsets
from records.models import Record
from records.serializers import RecordSerializer


class RecordViewSet(viewsets.ModelViewSet):
    queryset = Record.objects.all()
    serializer_class = RecordSerializer
    search_fields = ['asset']
    filter_fields = ['name']

