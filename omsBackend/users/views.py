# -*- coding: utf-8 -*-
# author: kiven

from users.serializers import UserSerializer, GroupSerializer, RoleSerializer
from rest_framework import viewsets

from users.filters import UserFilter
from users.models import Group, User, Role


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_class = UserFilter
    ordering_fields = ('-create_date',)

class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer