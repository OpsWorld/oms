# -*- coding: utf-8 -*-
# author: itimor

from django_filters import rest_framework as filters
from menus.models import Firstmenu, Secondmenu, Element


class FirstmenuFilter(filters.FilterSet):
    class Meta:
        model = Firstmenu
        fields = {
            'id': ['exact'],
            'title': ['exact'],
            'name': ['exact'],
        }


class SecondmenuFilter(filters.FilterSet):
    class Meta:
        model = Secondmenu
        fields = {
            'id': ['exact'],
            'title': ['exact'],
            'name': ['exact'],
            'parent__title': ['exact'],
        }


class ElementFilter(filters.FilterSet):
    class Meta:
        model = Element
        fields = {
            'id': ['exact'],
            'name': ['exact', 'contains'],
            'code': ['exact'],
            'parent__title': ['exact'],
        }
