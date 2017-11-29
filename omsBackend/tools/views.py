# -*- coding: utf-8 -*-
# author: itimor

from rest_framework import viewsets
from tools.models import Upload
from tools.serializers import UploadSerializer
from tools.filters import UploadFilter

class UploadViewSet(viewsets.ModelViewSet):
    queryset = Upload.objects.all()
    serializer_class = UploadSerializer
    filter_class = UploadFilter
