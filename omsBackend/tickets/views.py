# -*- coding: utf-8 -*-
# author: kiven

from rest_framework import viewsets
from tickets.models import WorkTicket, TicketComment, TicketEnclosure, TicketType, TicketWiki
from tickets.serializers import WorkTicketSerializer, TicketCommentSerializer, TicketEnclosureSerializer, \
    TicketTypeSerializer, TicketWikiSerializer
from tickets.filters import WorkTicketFilter, TicketCommentFilter


class WorkTicketViewSet(viewsets.ModelViewSet):
    queryset = WorkTicket.objects.all().order_by('-create_time')
    serializer_class = WorkTicketSerializer
    filter_class = WorkTicketFilter


class TicketCommentViewSet(viewsets.ModelViewSet):
    queryset = TicketComment.objects.all().order_by('-create_time')
    serializer_class = TicketCommentSerializer
    filter_class = TicketCommentFilter


class TicketEnclosureViewSet(viewsets.ModelViewSet):
    queryset = TicketEnclosure.objects.all()
    serializer_class = TicketEnclosureSerializer


class TicketTypeViewSet(viewsets.ModelViewSet):
    queryset = TicketType.objects.all()
    serializer_class = TicketTypeSerializer


class TicketWikiViewSet(viewsets.ModelViewSet):
    queryset = TicketWiki.objects.all()
    serializer_class = TicketWikiSerializer
