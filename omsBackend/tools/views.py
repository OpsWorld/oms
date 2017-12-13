# -*- coding: utf-8 -*-
# author: itimor

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from tools.models import Upload, Sendmail
from tools.serializers import UploadSerializer, SendmailSerializer
from tools.filters import UploadFilter
from cmd.cmdrun import run

class UploadViewSet(viewsets.ModelViewSet):
    queryset = Upload.objects.all()
    serializer_class = UploadSerializer
    filter_class = UploadFilter


class SendmailViewSet(viewsets.ModelViewSet):
    queryset = Sendmail.objects.all()
    serializer_class = SendmailSerializer

    def create(self, request, *args, **kwargs):
        serializer = SendmailSerializer(data=request.data, context={'request': request})
        to = request.data["to"]
        cc = request.data["cc"]
        sub = request.data["sub"]
        content = request.data["content"]
        cmd = '/root/.pyenv/versions/envoms/bin/python /data/projects/oms/omsBackend/utils/sendmail.py {} {} {} {}'.format(to, cc, sub, content)
        print(cmd)
        results = run(cmd).stdout
        print(results)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
