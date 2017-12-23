# -*- coding: utf-8 -*-
# author: kiven

from rest_framework import viewsets
from threepay.models import Platform, Merchant, ThreePayEnclosure, PayChannelName, PayChannel
from threepay.serializers import (PlatformSerializer,
                                  MerchantSerializer,
                                  PayChannelNameSerializer,
                                  PayChannelSerializer,
                                  ThreePayEnclosureSerializer)
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter


class PlatformViewSet(viewsets.ModelViewSet):
    queryset = Platform.objects.all()
    serializer_class = PlatformSerializer


class MerchantViewSet(viewsets.ModelViewSet):
    queryset = Merchant.objects.all()
    serializer_class = MerchantSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filter_fields = ('platform__name', 'name')


class PayChannelNameViewSet(viewsets.ModelViewSet):
    queryset = PayChannelName.objects.all()
    serializer_class = PayChannelNameSerializer

class PayChannelViewSet(viewsets.ModelViewSet):
    queryset = PayChannel.objects.all()
    serializer_class = PayChannelSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filter_fields = ('platform__name', 'merchant__name', 'type__name')


class ThreePayEnclosureViewSet(viewsets.ModelViewSet):
    queryset = ThreePayEnclosure.objects.all()
    serializer_class = ThreePayEnclosureSerializer
