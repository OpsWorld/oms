# -*- coding: utf-8 -*-
# author: kiven

from django_filters import rest_framework as filters
from users.models import User, Group, Role

class UserFilter(filters.FilterSet):
    class Meta:
        model = User
        fields = {
            'id': ['gt'],
            'username': ['exact', 'contains'],
            'email': ['exact'],
            'group__name': ['exact'],
            'is_active': ['exact'],
            'roles__cnname': ['exact'],
        }

class GroupFilter(filters.FilterSet):
    class Meta:
        model = Group
        fields = {
            'name': ['exact', 'contains'],
        }

class RoleFilter(filters.FilterSet):
    class Meta:
        model = Role
        fields = {
            'name': ['exact', 'contains'],
        }
