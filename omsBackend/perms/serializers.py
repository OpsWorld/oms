# -*- coding: utf-8 -*-
# author: itimor

from rest_framework import serializers

from perms.models import UserMenuPerms
from menus.models import Firstmenu, Secondmenu, Element
from users.models import Group

class UserMenuPermsSerializer(serializers.ModelSerializer):
    group = serializers.SlugRelatedField(queryset=Group.objects.all(), slug_field='name', allow_null=True)
    firstmenus = serializers.SlugRelatedField(many=True, queryset=Firstmenu.objects.all(), slug_field='title', allow_null=True)
    secondmenus = serializers.SlugRelatedField(many=True, queryset=Secondmenu.objects.all(), slug_field='title', allow_null=True)
    elements = serializers.SlugRelatedField(many=True, queryset=Element.objects.all(), slug_field='name', allow_null=True)

    class Meta:
        model = UserMenuPerms
        fields = ('url', 'id', 'group', 'firstmenus', 'secondmenus', 'elements')