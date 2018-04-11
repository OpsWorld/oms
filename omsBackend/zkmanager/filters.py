# -*- coding: utf-8 -*-
# author: itimor

from .models import Punch
from django_filters import rest_framework as filters
from django_filters import DateFromToRangeFilter


class PunchFilter(filters.FilterSet):
    create_date = DateFromToRangeFilter()

    class Meta:
        model = Punch
        fields = ['create_date', 'user_id__username']
