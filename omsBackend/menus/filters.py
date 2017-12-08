# -*- coding: utf-8 -*-
# author: itimor

from django_filters import rest_framework as filters
from menus.models import Firstmenu, Secondmenu, MenuMeta


class FirstmenuFilter(filters.FilterSet):
    class Meta:
        model = Firstmenu
        fields = {
            'id': ['exact'],
            'group': ['exact'],
        }


class SecondmenuFilter(filters.FilterSet):
    class Meta:
        model = Secondmenu
        fields = {
            'id': ['exact'],
            'group': ['exact'],
        }


class MenuMetaFilter(filters.FilterSet):
    class Meta:
        model = MenuMeta
        fields = {
            'id': ['exact'],
            'group': ['exact'],
        }
