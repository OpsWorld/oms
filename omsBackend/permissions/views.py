# -*- coding: utf-8 -*-
# author: kiven

from rest_framework import viewsets
from permissions.models import Firstmenu, Secondmenu, MenuMeta
from permissions.serializers import FirstmenuSerializer, SecondmenuSerializer, MenuMetaSerializer


class FirstmenuViewSet(viewsets.ModelViewSet):
    queryset = Firstmenu.objects.all()
    serializer_class = FirstmenuSerializer


class SecondmenuViewSet(viewsets.ModelViewSet):
    queryset = Secondmenu.objects.all()
    serializer_class = SecondmenuSerializer


class MenuMateViewSet(viewsets.ModelViewSet):
    queryset = MenuMeta.objects.all()
    serializer_class = MenuMetaSerializer
