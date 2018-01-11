# -*- coding: utf-8 -*-
# author: itimor

from rest_framework import viewsets
from jobs.models import Jobs, Deployenv, DeployJobs
from jobs.serializers import JobsSerializer, DeployenvSerializer, DeployJobsSerializer


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

    # def list(self, request, *args, **kwargs):
    #     serializer = DeployJobsSerializer(data=request.data, context={'request': request})
    #     # works = DeployJobs.objects.all().filter(deploy_status='deploy')
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)