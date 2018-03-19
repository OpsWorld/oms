# -*- coding: utf-8 -*-
# author: itimor

from projects.models import admin_groups, Project
from users.models import User
from django.db.models import Q
from dry_rest_permissions.generics import DRYPermissionFiltersBase

from django_filters import rest_framework as filters
from django_filters import DateFromToRangeFilter
from projects.models import Project


class ProjectFilter(filters.FilterSet):
    create_date = DateFromToRangeFilter()
    update_date = DateFromToRangeFilter()

    class Meta:
        model = Project
        fields = ['pid', 'status', 'demand__name', 'action_user__username', 'create_date', 'update_date']


class ProjectFilterBackend(DRYPermissionFiltersBase):
    def filter_list_queryset(self, request, queryset, view):
        """
        Limits all list requests to only be seen by the create_groups.
        admin groups can get all().
        """
        groups = User.objects.get(username=request.user).groups.all()
        group_list = [group.name for group in groups]

        # 求交集
        is_admin = [i for i in group_list if i in admin_groups]
        if len(is_admin) > 0:
            return queryset
        else:
            return queryset.filter(
                (
                    (
                        Q(create_user=request.user) |
                        Q(action_user__username__contains=request.user) |
                        Q(follow_user__username__contains=request.user)
                    ) &
                    Q(is_public=False)
                ) |
                Q(is_public=True)
            ).distinct()
