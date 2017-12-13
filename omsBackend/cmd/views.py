# -*- coding: utf-8 -*-
# author: itimor

from rest_framework.response import Response
from rest_framework import viewsets
from cmd.models import Cmdrun
from cmd.serializers import CmdrunSerializer
from cmd.cmdrun import run
from rest_framework import status

class CmdrunViewSet(viewsets.ModelViewSet):
    queryset = Cmdrun.objects.all()
    serializer_class = CmdrunSerializer

    def create(self, request, *args, **kwargs):
        serializer = CmdrunSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            cmd = serializer.data['cmd']
            results = run(cmd).stdout
            return Response({'results':results}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)