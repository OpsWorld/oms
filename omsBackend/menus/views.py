# -*- coding: utf-8 -*-
# author: kiven

from rest_framework import viewsets
from menus.models import Firstmenu, Secondmenu, Element
from menus.serializers import FirstmenuSerializer, SecondmenuSerializer, ElementSerializer
from menus.filters import FirstmenuFilter, SecondmenuFilter, ElementFilter


class FirstmenuViewSet(viewsets.ModelViewSet):
    queryset = Firstmenu.objects.all()
    serializer_class = FirstmenuSerializer
    filter_class = FirstmenuFilter


class SecondmenuViewSet(viewsets.ModelViewSet):
    queryset = Secondmenu.objects.all()
    serializer_class = SecondmenuSerializer
    filter_class = SecondmenuFilter


class ElementViewSet(viewsets.ModelViewSet):
    queryset = Element.objects.all()
    serializer_class = ElementSerializer
    filter_class = ElementFilter
