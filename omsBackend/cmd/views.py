# -*- coding: utf-8 -*-
# author: itimor

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from cmd.models import Cmdrun
from cmd.serializers import CmdrunSerializer
from cmd.cmdrun import run

class CmdrunViewSet(viewsets.ModelViewSet):
    queryset = Cmdrun.objects.all()
    serializer_class = CmdrunSerializer

    def create(self, request, *args, **kwargs):
        serializer = CmdrunSerializer(data=request.data, context={'request': request})
        cmd = request.data["cmd"]
        results = run(cmd).stdout
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)