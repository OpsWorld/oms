# -*- coding: utf-8 -*-
# author: itimor

from rest_framework import viewsets
from perms.models import UserMenuPerms, UserHostPerms
from perms.serializers import UserMenuPermsSerializer, UserHostPermsSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from users.models import User, Group
from users.serializers import UserSerializer, RoleSerializer, GroupSerializer
from perms.filters import UserMenuPermsFilter


class UserMenuPermsViewSet(viewsets.ModelViewSet):
    queryset = UserMenuPerms.objects.all()
    serializer_class = UserMenuPermsSerializer
    filter_class = UserMenuPermsFilter


@api_view()
def routers(request, username=None):
    userqueryset = User.objects.get(username=username)
    userserializer = UserSerializer(userqueryset, context={'request': request}).data
    groups = userserializer['groups']
    menus = []
    elements = []
    for group in groups:
        try:
            menuqueryset = UserMenuPerms.objects.get(group=group)
            menuserializer = UserMenuPermsSerializer(menuqueryset, context={'request': request}).data
            menus = menuserializer["firstmenus"] + menuserializer["secondmenus"] + menus
            elements = menuserializer["elements"] + elements
        except Exception as e:
            pass
    menus = set(menus)
    elements = set(elements)
    return Response({"groups": groups, "menus": menus, "elements": elements})


class UserHostPermsViewSet(viewsets.ModelViewSet):
    queryset = UserHostPerms.objects.all()
    serializer_class = UserHostPermsSerializer