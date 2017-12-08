# -*- coding: utf-8 -*-
# author: itimor

from menus.models import Firstmenu, Secondmenu, MenuMeta
from rest_framework import serializers


class MenuMetaSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuMeta
        fields = ('url', 'id', 'name')


class SecondmenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Secondmenu
        fields = ('url', 'id', 'name', 'path', 'component', 'hidden', 'meta')


class FirstmenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Firstmenu
        fields = ('url', 'id', 'name', 'path', 'component', 'icon', 'redirect', 'hidden', 'children', 'meta')
