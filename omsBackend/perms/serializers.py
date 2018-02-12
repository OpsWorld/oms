# -*- coding: utf-8 -*-
# author: itimor

from rest_framework import serializers

from perms.models import UserMenuPerms, UserHostPerms
from menus.models import Firstmenu, Secondmenu, Element
from users.models import Group
from hosts.models import Host


class UserMenuPermsSerializer(serializers.ModelSerializer):
    firstmenus = serializers.SlugRelatedField(many=True, queryset=Firstmenu.objects.all(), slug_field='title',
                                              allow_null=True)
    secondmenus = serializers.SlugRelatedField(many=True, queryset=Secondmenu.objects.all(), slug_field='title',
                                               allow_null=True)
    elements = serializers.SlugRelatedField(many=True, queryset=Element.objects.all(), slug_field='name',
                                            allow_null=True)

    class Meta:
        model = UserMenuPerms
        fields = ('url', 'id', 'group', 'firstmenus', 'secondmenus', 'elements')


class UserHostPermsSerializer(serializers.ModelSerializer):
    usergroups = serializers.SlugRelatedField(queryset=Group.objects.all(), slug_field='name')
    hosts = serializers.SlugRelatedField(many=True, queryset=Host.objects.all(), slug_field='hostname')

    class Meta:
        model = UserHostPerms
        fields = ('url', 'id', 'name', 'usergroups', 'hosts')