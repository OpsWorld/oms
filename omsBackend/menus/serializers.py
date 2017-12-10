# -*- coding: utf-8 -*-
# author: itimor

from menus.models import Firstmenu, Secondmenu, Element
from rest_framework import serializers


class ElementSerializer(serializers.ModelSerializer):
    parent = serializers.SlugRelatedField(queryset=Secondmenu.objects.all(), slug_field='title', allow_null=True)

    class Meta:
        model = Element
        fields = ('url', 'id', 'parent', 'name', 'code')


class SecondmenuSerializer(serializers.ModelSerializer):
    parent = serializers.SlugRelatedField(queryset=Firstmenu.objects.all(), slug_field='title', allow_null=True)

    class Meta:
        model = Secondmenu
        fields = ('url', 'id', 'title', 'name', 'path', 'component', 'hidden', 'parent')


class FirstmenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Firstmenu
        fields = ('url', 'id', 'title', 'name', 'path', 'component', 'icon', 'redirect', 'hidden')
