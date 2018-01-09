# -*- coding: utf-8 -*-
# author: kiven

from rest_framework import viewsets
from worktickets.models import WorkTicket, TicketComment, TicketEnclosure, TicketType
from worktickets.serializers import (WorkTicketSerializer,
                                     TicketCommentSerializer,
                                     TicketEnclosureSerializer,
                                     TicketTypeSerializer)
from worktickets.filters import WorkTicketFilterBackend
from dry_rest_permissions.generics import DRYPermissions

class WorkTicketViewSet(viewsets.ModelViewSet):
    queryset = WorkTicket.objects.all().order_by('ticket_status')
    serializer_class = WorkTicketSerializer
    search_fields = ['title', 'content', 'type__name']
    filter_fields = ['ticket_status','ticketid','create_user__username','action_user__username']
    filter_backends = (WorkTicketFilterBackend,)
    permission_classes = (DRYPermissions,)


class TicketCommentViewSet(viewsets.ModelViewSet):
    queryset = TicketComment.objects.all()
    serializer_class = TicketCommentSerializer
    filter_fields = ['ticket__ticketid']


class TicketEnclosureViewSet(viewsets.ModelViewSet):
    queryset = TicketEnclosure.objects.all()
    serializer_class = TicketEnclosureSerializer
    filter_fields = ['ticket__ticketid']


class TicketTypeViewSet(viewsets.ModelViewSet):
    queryset = TicketType.objects.all()
    serializer_class = TicketTypeSerializer
