# -*- coding: utf-8 -*-
# author: itimor

from rest_framework import viewsets
from tools.models import Upload, Sendmail
from tools.serializers import UploadSerializer, SendmailSerializer
from tools.filters import UploadFilter

class UploadViewSet(viewsets.ModelViewSet):
    queryset = Upload.objects.all()
    serializer_class = UploadSerializer
    filter_class = UploadFilter


class SendmailViewSet(viewsets.ModelViewSet):
    queryset = Sendmail.objects.all()
    serializer_class = SendmailSerializer
