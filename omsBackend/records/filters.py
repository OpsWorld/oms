# -*- coding: utf-8 -*-
# author: itimor

from django_filters import rest_framework as filters
from django_filters import DateTimeFromToRangeFilter
from records.models import Record


class RecordFilter(filters.FilterSet):
    create_time = DateTimeFromToRangeFilter()

    class Meta:
        model = Record
        fields = ['name', 'create_time']
