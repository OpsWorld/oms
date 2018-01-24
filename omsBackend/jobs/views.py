# -*- coding: utf-8 -*-
# author: itimor

from rest_framework import viewsets
from jobs.models import Jobs, DeployJobs
from jobs.serializers import JobsSerializer, DeployJobsSerializer
from omsBackend.settings import sapi
from jobs.filters import JobFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.decorators import api_view
from rest_framework.response import Response


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


@api_view()
def update_jobs_status(request):
    try:
        job__name = request.GET['job__name']
        jobs = DeployJobs.objects.filter(job__name=job__name).filter(deploy_status='deploy')
        count = len(jobs)
        print(count)
        for job in jobs:
            print(job)
            j_id = job.j_id
            j = DeployJobs.objects.get(j_id=j_id)
            job_status = sapi.check_job(j_id)
            print(job_status)
            try:
                if list(set(job_status.values()))[0]:
                    j.result = sapi.get_result(j_id)
                    j.deploy_status = 'success'
                else:
                    j.deploy_status = 'deploy'
            except Exception as e:
                pass
            j.save()
        return Response({"results": 'success', "count": count})
    except Exception as e:
        return Response({"results": '?job__name=ttt', "count": 1024})
