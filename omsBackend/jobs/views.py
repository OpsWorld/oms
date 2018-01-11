# -*- coding: utf-8 -*-
# author: itimor

from rest_framework import viewsets
from jobs.models import Jobs, Deployenv, DeployJobs
from jobs.serializers import JobsSerializer, DeployenvSerializer, DeployJobsSerializer
from celery.result import AsyncResult


class JobsViewSet(viewsets.ModelViewSet):
    queryset = Jobs.objects.all()
    serializer_class = JobsSerializer


class DeployenvViewSet(viewsets.ModelViewSet):
    queryset = Deployenv.objects.all()
    serializer_class = DeployenvSerializer
    filter_fields = ['job__name']


class DeployJobsViewSet(viewsets.ModelViewSet):
    queryset = DeployJobs.objects.all().order_by('-create_time')
    serializer_class = DeployJobsSerializer