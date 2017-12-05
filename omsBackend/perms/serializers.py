# -*- coding: utf-8 -*-
# author: itimor

from rest_framework import serializers

from perms.models import UserMenuPerms
from menus.models import Firstmenu, Secondmenu
from users.models import User

class UserMenuPermsSerializer(serializers.ModelSerializer):
    firstmenus = serializers.SlugRelatedField(many=True, queryset=Firstmenu.objects.all(), slug_field='name', allow_null=True)
    seaondmenus = serializers.SlugRelatedField(many=True, queryset=Secondmenu.objects.all(), slug_field='name', allow_null=True)
    user = serializers.SlugRelatedField(queryset=User.objects.all(), slug_field='username', allow_null=True)

    class Meta:
        model = UserMenuPerms
        fields = ('url', 'id', 'user', 'firstmenus', 'seaondmenus')