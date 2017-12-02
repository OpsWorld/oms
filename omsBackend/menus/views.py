# -*- coding: utf-8 -*-
# author: kiven

from rest_framework import viewsets
from menus.models import Firstmenu, Secondmenu, MenuMeta
from menus.serializers import FirstmenuSerializer, SecondmenuSerializer, MenuMetaSerializer


class FirstmenuViewSet(viewsets.ModelViewSet):
    queryset = Firstmenu.objects.all()
    serializer_class = FirstmenuSerializer


class SecondmenuViewSet(viewsets.ModelViewSet):
    queryset = Secondmenu.objects.all()
    serializer_class = SecondmenuSerializer


class MenuMetaViewSet(viewsets.ModelViewSet):
    queryset = MenuMeta.objects.all()
    serializer_class = MenuMetaSerializer
