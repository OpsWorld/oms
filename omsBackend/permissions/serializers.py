# -*- coding: utf-8 -*-
# author: itimor

from permissions.models import Firstmenu, Secondmenu, MenuMate
from rest_framework import serializers


class MenuMateSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuMate
        fields = ('url', 'id', 'name', 'action')


class FirstmenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Firstmenu
        fields = ('url', 'id', 'name', 'path', 'component', 'icon', 'redirect', 'hidden', 'mate')


class SecondmenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Secondmenu
        fields = ('url', 'id', 'name', 'path', 'component', 'hidden', 'parent', 'mate')
