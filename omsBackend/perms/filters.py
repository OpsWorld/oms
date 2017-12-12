# -*- coding: utf-8 -*-
# author: itimor

from django_filters import rest_framework as filters
from perms.models import UserMenuPerms

class UserMenuPermsFilter(filters.FilterSet):
    class Meta:
        model = UserMenuPerms
        fields = {
            'id': ['exact'],
            'group': ['exact'],
            'secondmenus__title': ['exact', 'contains'],
        }