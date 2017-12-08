# -*- coding: utf-8 -*-
# author: kiven

from rest_framework import viewsets
from menus.models import Firstmenu, Secondmenu, MenuMeta
from menus.serializers import FirstmenuSerializer, SecondmenuSerializer, MenuMetaSerializer
from menus.models import FirstmenuFilter, SecondmenuFilter, MenuMetaFilter


class FirstmenuViewSet(viewsets.ModelViewSet):
    queryset = Firstmenu.objects.all()
    serializer_class = FirstmenuSerializer
    filter_class = FirstmenuFilter


class SecondmenuViewSet(viewsets.ModelViewSet):
    queryset = Secondmenu.objects.all()
    serializer_class = SecondmenuSerializer
    filter_class = SecondmenuFilter


class MenuMetaViewSet(viewsets.ModelViewSet):
    queryset = MenuMeta.objects.all()
    serializer_class = MenuMetaSerializer
    filter_class = MenuMetaFilter
