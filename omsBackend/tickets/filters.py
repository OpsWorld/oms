# -*- coding: utf-8 -*-
# author: kiven

from django_filters import rest_framework as filters
from tickets.models import WorkTicket

class WorkTicketFilter(filters.FilterSet):
    class Meta:
        model = WorkTicket
        fields = {
            'id': ['exact'],
            'title': ['exact', 'contains'],
            'type__name': ['exact'],
            'create_user__username': ['exact'],
            'action_user__username': ['exact'],
            'create_time': ['exact', 'contains'],
            'level': ['exact'],
            'ticket_status': ['exact'],
        }