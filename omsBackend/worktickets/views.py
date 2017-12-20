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

from worktickets.models import Platform, Merchant, PlatformEnclosure, ThreePayTicket, PayChannel
from worktickets.serializers import (PlatformSerializer,
                                     MerchantSerializer,
                                     PayChannelSerializer,
                                     PlatformEnclosureSerializer,
                                     ThreePayTicketSerializer)
from worktickets.filters import WorkTicketFilter, TicketCommentFilter, TicketEnclosureFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter


class WorkTicketViewSet(viewsets.ModelViewSet):
    queryset = WorkTicket.objects.all().order_by('-create_time')
    serializer_class = WorkTicketSerializer
    # filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    # filter_fields = ('ticketid', 'create_user__username', 'action_user__username', 'level','ticket_status')
    # search_fields = ('title', 'content', 'type__name')
    # ordering_fields = ('id', 'create_time')
    filter_class = WorkTicketFilter
    filter_backends = (DjangoFilterBackend, SearchFilter,)
    search_fields = ('title', 'content', 'type__name')


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


class ThreePayTicketViewSet(viewsets.ModelViewSet):
    queryset = ThreePayTicket.objects.all()
    serializer_class = ThreePayTicketSerializer


class PlatformViewSet(viewsets.ModelViewSet):
    queryset = Platform.objects.all()
    serializer_class = PlatformSerializer


class PayChannelViewSet(viewsets.ModelViewSet):
    queryset = PayChannel.objects.all()
    serializer_class = PayChannelSerializer


class MerchantViewSet(viewsets.ModelViewSet):
    queryset = Merchant.objects.all()
    serializer_class = MerchantSerializer


class PlatformEnclosureViewSet(viewsets.ModelViewSet):
    queryset = PlatformEnclosure.objects.all()
    serializer_class = PlatformEnclosureSerializer
