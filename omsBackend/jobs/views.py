# -*- coding: utf-8 -*-
# author: itimor

from rest_framework import viewsets
from jobs.models import Jobs, Deployenv, DeployJobs
from jobs.serializers import JobsSerializer, DeployenvSerializer, DeployJobsSerializer
from celery.result import AsyncResult
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

    def list(self, request, *args, **kwargs):
        works = DeployJobs.objects.all().filter(deploy_status='deploy')
        deploy_serializer = DeployJobsSerializer(works, many=True, context={'request': request})
        for work in deploy_serializer.data:
            j_id = work['j_id']
            j = DeployJobs.objects.get(j_id=j_id)
            job = AsyncResult(j_id)
            if job.ready():  # check task state: true/false
                try:
                    result = job.get(timeout=1)
                    print(result)
                    if job.state in ['PENDING ','STARTED ']:
                        j.deploy_status = 'deploy'
                    elif job.state == 'SUCCESS':
                        j.deploy_status = 'success'
                    else:
                        j.deploy_status = 'failed'
                    j.save()
                except:
                    pass

        queryset = DeployJobs.objects.all().order_by('-create_time')
        serializer = DeployJobsSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)