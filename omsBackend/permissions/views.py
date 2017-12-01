# -*- coding: utf-8 -*-
# author: kiven

from rest_framework import viewsets
from permissions.models import Firstmenu, Secondmenu, MenuMate
from permissions.serializers import FirstmenuSerializer, SecondmenuSerializer, MenuMateSerializer


class FirstmenuViewSet(viewsets.ModelViewSet):
    queryset = Firstmenu.objects.all()
    serializer_class = FirstmenuSerializer


class SecondmenuViewSet(viewsets.ModelViewSet):
    queryset = Secondmenu.objects.all()
    serializer_class = SecondmenuSerializer


class MenuMateViewSet(viewsets.ModelViewSet):
    queryset = MenuMate.objects.all()
    serializer_class = MenuMateSerializer
