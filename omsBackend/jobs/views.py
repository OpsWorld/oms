# -*- coding: utf-8 -*-
# author: itimor

from rest_framework import viewsets
from jobs.models import Jobs, Deployenv
from jobs.serializers import JobsSerializer, DeployenvSerializer

class JobsViewSet(viewsets.ModelViewSet):
    queryset = Jobs.objects.all()
    serializer_class = JobsSerializer


class DeployenvViewSet(viewsets.ModelViewSet):
    queryset = Deployenv.objects.all()
    serializer_class = DeployenvSerializer
