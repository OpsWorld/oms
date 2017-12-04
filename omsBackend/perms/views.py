# -*- coding: utf-8 -*-
# author: itimor

from rest_framework import viewsets
from perms.models import UserMenuPerms
from perms.serializers import UserMenuPermsSerializer
from rest_framework.response import Response

class UserMenuPermsViewSet(viewsets.ModelViewSet):
    queryset = UserMenuPerms.objects.all()
    serializer_class = UserMenuPermsSerializer

    def retrieve(self, request, *args, **kwargs):
        serializer = UserMenuPermsSerializer(data=request.data)
        print(serializer)
        return Response({'something': 'my custom JSON'})

