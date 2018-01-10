# -*- coding: utf-8 -*-
# author: itimor

from rest_framework import viewsets
from jobs.models import Jobs, Deployenv, DeployJobs
from jobs.serializers import JobsSerializer, DeployenvSerializer, DeployJobsSerializer
from celery.result import AsyncResult
from tasks.tasks import salt_run_cmd
from rest_framework.response import Response
from rest_framework import status


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

    def create(self, request, *args, **kwargs):
        serializer = DeployJobsSerializer(data=request.data, context={'request': request})
        hosts = request.data["hosts"]
        version = request.data["version"]
        cmd = 'svn up -r %s' % version
        deploy_path = request.data["deploy_path"]
        salt_run_cmd.delay(hosts, cmd, deploy_path)

        return Response({"code": "1024"}, status=status.HTTP_201_CREATED)
