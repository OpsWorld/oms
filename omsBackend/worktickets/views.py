# -*- coding: utf-8 -*-
# author: kiven

from rest_framework import viewsets
from worktickets.models import WorkTicket, TicketComment, TicketEnclosure, TicketType
from worktickets.serializers import (WorkTicketSerializer,
                                     TicketCommentSerializer,
                                     TicketEnclosureSerializer,
                                     TicketTypeSerializer)
from worktickets.filters import WorkTicketFilterBackend
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from dry_rest_permissions.generics import DRYPermissions

class WorkTicketViewSet(viewsets.ModelViewSet):
    queryset = WorkTicket.objects.all().order_by('ticket_status','-create_time','-update_time')
    serializer_class = WorkTicketSerializer
    filter_backends = (WorkTicketFilterBackend,DjangoFilterBackend, SearchFilter, OrderingFilter)
    search_fields = ('title', 'content', 'type__name')
    ordering_fields = ('level', 'ticket_status','create_time','update_time')
    filter_fields = ('ticket_status','ticketid','create_user__username','action_user__username')
    permission_classes = (DRYPermissions,)


class TicketCommentViewSet(viewsets.ModelViewSet):
    queryset = TicketComment.objects.all()
    serializer_class = TicketCommentSerializer
    filter_fields = ('ticket__ticketid',)


class TicketEnclosureViewSet(viewsets.ModelViewSet):
    queryset = TicketEnclosure.objects.all()
    serializer_class = TicketEnclosureSerializer
    filter_fields = ('ticket__ticketid',)


class TicketTypeViewSet(viewsets.ModelViewSet):
    queryset = TicketType.objects.all()
    serializer_class = TicketTypeSerializer
