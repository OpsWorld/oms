# -*- coding: utf-8 -*-
# author: itimor

from rest_framework import serializers

from perms.models import UserMenuPerms
from menus.models import Firstmenu, Secondmenu, MenuMeta

class UserMenuPermsSerializer(serializers.ModelSerializer):
    firstmenus = serializers.SlugRelatedField(many=True, queryset=Firstmenu.objects.all(), slug_field='name', allow_null=True)
    secondmenus = serializers.SlugRelatedField(many=True, queryset=Secondmenu.objects.all(), slug_field='name', allow_null=True)
    elements = serializers.SlugRelatedField(many=True, queryset=MenuMeta.objects.all(), slug_field='name', allow_null=True)

    class Meta:
        model = UserMenuPerms
        fields = ('url', 'id', 'group', 'firstmenus', 'secondmenus', 'elements')