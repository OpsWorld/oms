# -*- coding: utf-8 -*-
# author: kiven

from django_filters import rest_framework as filters
from worktickets.models import WorkTicket
from users.models import User
from dry_rest_permissions.generics import DRYPermissionFiltersBase

class WorkTicketFilter(filters.FilterSet):
    class Meta:
        model = WorkTicket
        fields = {
            'ticketid': ['exact'],
            'title': ['exact', 'contains'],
            'content': ['contains'],
            'create_user__username': ['exact'],
            'action_user__username': ['exact'],
            'level': ['exact'],
            'ticket_status': ['exact'],
        }

admin_groups = ['admin']

class WorkTicketFilterBackend(DRYPermissionFiltersBase):
    def filter_list_queryset(self, request, queryset, view):
        """
        Limits all list requests to only be seen by the create_groups.
        admin groups can get all().
        """
        groups = User.objects.get(username=request.user).groups.all()
        admin_list = [group.name for group in groups]

        #求交集
        is_admin = [i for i in admin_list if i in admin_groups]
        if len(is_admin) > 0:
            return queryset
        else:
            return queryset.filter(create_group__in=groups)
