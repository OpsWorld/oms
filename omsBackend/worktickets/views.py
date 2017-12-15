# -*- coding: utf-8 -*-
# author: kiven

from rest_framework import viewsets
from worktickets.models import WorkTicket, TicketComment, TicketEnclosure, TicketType, TicketWiki
from worktickets.serializers import (WorkTicketSerializer,
                                     TicketCommentSerializer,
                                     TicketEnclosureSerializer,
                                     TicketTypeSerializer,
                                     TicketWikiSerializer)
from worktickets.filters import WorkTicketFilter, TicketCommentFilter, TicketEnclosureFilter

from worktickets.models import Platform, Merchant, ThreePayEnclosure
from worktickets.serializers import (PlatformSerializer,
                                     MerchantSerializer,
                                     ThreePayEnclosureSerializer,)
from worktickets.filters import WorkTicketFilter, TicketCommentFilter, TicketEnclosureFilter

class WorkTicketViewSet(viewsets.ModelViewSet):
    queryset = WorkTicket.objects.all().order_by('-create_time')
    serializer_class = WorkTicketSerializer
    filter_class = WorkTicketFilter


class TicketCommentViewSet(viewsets.ModelViewSet):
    queryset = TicketComment.objects.all()
    serializer_class = TicketCommentSerializer
    filter_class = TicketCommentFilter


class TicketEnclosureViewSet(viewsets.ModelViewSet):
    queryset = TicketEnclosure.objects.all()
    serializer_class = TicketEnclosureSerializer
    filter_class = TicketEnclosureFilter


class TicketTypeViewSet(viewsets.ModelViewSet):
    queryset = TicketType.objects.all()
    serializer_class = TicketTypeSerializer


class TicketWikiViewSet(viewsets.ModelViewSet):
    queryset = TicketWiki.objects.all()
    serializer_class = TicketWikiSerializer


class PlatformViewSet(viewsets.ModelViewSet):
    queryset = Platform.objects.all()
    serializer_class = PlatformSerializer

class MerchantViewSet(viewsets.ModelViewSet):
    queryset = Merchant.objects.all()
    serializer_class = MerchantSerializer

class ThreePayEnclosureViewSet(viewsets.ModelViewSet):
    queryset = ThreePayEnclosure.objects.all()
    serializer_class = ThreePayEnclosureSerializer