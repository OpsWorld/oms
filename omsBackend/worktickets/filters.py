# -*- coding: utf-8 -*-
# author: kiven

from django_filters import rest_framework as filters
from worktickets.models import WorkTicket, TicketComment, TicketEnclosure

class WorkTicketFilter(filters.FilterSet):
    class Meta:
        model = WorkTicket
        fields = {
            'id': ['exact'],
            'title': ['exact', 'contains'],
            'content': ['contains'],
            'type__name': ['exact'],
            'create_user__username': ['exact'],
            'action_user__username': ['exact'],
            'create_time': ['exact', 'contains'],
            'level': ['exact'],
            'ticket_status': ['exact'],
        }

class TicketCommentFilter(filters.FilterSet):
    class Meta:
        model = TicketComment
        fields = {
            'ticket__id': ['exact'],
        }

class TicketEnclosureFilter(filters.FilterSet):
    class Meta:
        model = TicketEnclosure
        fields = {
            'ticket__id': ['exact'],
        }