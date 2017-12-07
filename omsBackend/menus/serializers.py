# -*- coding: utf-8 -*-
# author: itimor

from menus.models import Firstmenu, Secondmenu, MenuMeta
from rest_framework import serializers


class MenuMetaSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuMeta
        fields = ('url', 'id', 'name', 'action')


class FirstmenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Firstmenu
        fields = ('url', 'id', 'name', 'path', 'component', 'icon', 'redirect', 'hidden', 'meta')


class SecondmenuSerializer(serializers.ModelSerializer):
    parent = serializers.SlugRelatedField(queryset=Firstmenu.objects.all(), slug_field='name')

    class Meta:
        model = Secondmenu
        fields = ('url', 'id', 'name', 'path', 'component', 'hidden', 'parent', 'meta')
