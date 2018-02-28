# -*- coding: utf-8 -*-
# author: itimor

from rest_framework import viewsets
from jobs.models import Jobs, Deployenv, Deploycmd, DeployJobs, DeployVersion, DeployTicket, DeployTicketEnclosure
from jobs.serializers import (JobsSerializer, DeployenvSerializer, DeploycmdSerializer, DeployJobsSerializer,
                              DeployVersionSerializer, DeployTicketSerializer, DeployTicketEnclosureSerializer)
from omsBackend.settings import sapi
from jobs.filters import JobFilterBackend
from rest_framework.filters import SearchFilter, DjangoFilterBackend
from rest_framework.decorators import api_view
from rest_framework.response import Response


class JobsViewSet(viewsets.ModelViewSet):
    queryset = Jobs.objects.all().order_by('id')
    serializer_class = JobsSerializer
    filter_backends = (JobFilterBackend, SearchFilter, DjangoFilterBackend)
    filter_fields = ['showdev']
    search_fields = ('name', 'code_url')


class DeployenvViewSet(viewsets.ModelViewSet):
    queryset = Deployenv.objects.all().order_by('id')
    serializer_class = DeployenvSerializer
    filter_fields = ['job__id']


class DeploycmdViewSet(viewsets.ModelViewSet):
    queryset = Deploycmd.objects.all().order_by('id')
    serializer_class = DeploycmdSerializer
    filter_fields = ['env__id']


class DeployJobsViewSet(viewsets.ModelViewSet):
    queryset = DeployJobs.objects.all().order_by('-create_time')
    serializer_class = DeployJobsSerializer
    filter_fields = ['job__name']
    search_fields = ['version', 'content']


class DeployVersionViewSet(viewsets.ModelViewSet):
    queryset = DeployVersion.objects.all()
    serializer_class = DeployVersionSerializer
    filter_fields = ['job__name']


class DeployTicketViewSet(viewsets.ModelViewSet):
    queryset = DeployTicket.objects.all().order_by('id')
    serializer_class = DeployTicketSerializer


class DeployTicketEnclosureViewSet(viewsets.ModelViewSet):
    queryset = DeployTicketEnclosure.objects.all()
    serializer_class = DeployTicketEnclosureSerializer
    filter_fields = ('ticket__id',)


@api_view()
def update_jobs_status(request):
    try:
        job = request.GET['job__name']
        jobs = DeployJobs.objects.filter(job__name=job).filter(deploy_status='deploy')
        count = len(jobs)
        for job in jobs:
            print(job)
            j_id = job.j_id
            j = DeployJobs.objects.get(j_id=j_id)
            job_status = sapi.check_job(j_id)
            print(list(set(job_status.values()))[0])
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
        return Response({"results": '?job__name=wtf', "count": 1024})
