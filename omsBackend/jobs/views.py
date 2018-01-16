# -*- coding: utf-8 -*-
# author: itimor

from rest_framework import viewsets
from jobs.models import Jobs, Deployenv, DeployJobs
from jobs.serializers import JobsSerializer, DeployenvSerializer, DeployJobsSerializer
from celery.result import AsyncResult
from rest_framework.response import Response
from rest_framework import status
from omsBackend.settings import sapi

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

    def list(self, request, *args, **kwargs):
        works = DeployJobs.objects.all().filter(deploy_status='deploy')
        deploy_serializer = DeployJobsSerializer(works, many=True, context={'request': request})
        for work in deploy_serializer.data:
            j_id = work['j_id']
            j = DeployJobs.objects.get(j_id=j_id)
            jobs = sapi.check_job(j_id)
            job_status = []
            for i in jobs.values():
                job_status.append(i)

            if True in job_status:
                j.deploy_status = 'success'
            else:
                j.deploy_status = 'failed'

            j.result = jobs
            j.save()
        queryset = DeployJobs.objects.all().order_by('-create_time')
        serializer = DeployJobsSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)