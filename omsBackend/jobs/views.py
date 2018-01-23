# -*- coding: utf-8 -*-
# author: itimor

from rest_framework import viewsets
from jobs.models import Jobs, DeployJobs
from jobs.serializers import JobsSerializer, DeployJobsSerializer
from rest_framework.response import Response
from rest_framework import status
from omsBackend.settings import sapi
from jobs.filters import JobFilterBackend
from rest_framework.filters import SearchFilter
from django.db.models import Q


class JobsViewSet(viewsets.ModelViewSet):
    queryset = Jobs.objects.all()
    serializer_class = JobsSerializer
    filter_backends = (JobFilterBackend, SearchFilter)
    search_fields = ('name', 'code_url')


# class DeployenvViewSet(viewsets.ModelViewSet):
#     queryset = Deployenv.objects.all()
#     serializer_class = DeployenvSerializer
#     filter_fields = ['job__name']


class DeployJobsViewSet(viewsets.ModelViewSet):
    queryset = DeployJobs.objects.all().order_by('-create_time')
    serializer_class = DeployJobsSerializer
    filter_fields = ['job__name']
    search_fields = ['version', 'content']

    def list(self, request, *args, **kwargs):
        try:
            job_name = request.GET['job__name']
            search = request.GET['search']
            works = DeployJobs.objects.filter(job__name=job_name).filter(deploy_status='deploy')
            deploy_serializer = DeployJobsSerializer(works, many=True, context={'request': request})
            for work in deploy_serializer.data:
                j_id = work['j_id']
                j = DeployJobs.objects.get(j_id=j_id)
                job_status = sapi.check_job(j_id)
                print(job_status)

                try:
                    if list(set(job_status.values()))[0]:
                        j.result = sapi.get_result(j_id)
                        j.deploy_status = 'success'
                        import re
                        jdata = list(j.result.values())[0]
                        j.version = re.findall('At revision (\d+)', jdata)[0]
                    else:
                        j.deploy_status = 'deploy'
                except Exception as e:
                    pass

                j.save()
            if search:
                queryset = DeployJobs.objects.filter(job__name=job_name).filter(
                    Q(version=search) | Q(content__contains=search)).order_by('-create_time')
            else:
                queryset = DeployJobs.objects.filter(job__name=job_name).order_by('-create_time')
            serializer = DeployJobsSerializer(queryset, many=True, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            queryset = DeployJobs.objects.all().order_by('-create_time')
            serializer = DeployJobsSerializer(queryset, many=True, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
