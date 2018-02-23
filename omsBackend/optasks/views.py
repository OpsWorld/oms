# -*- coding: utf-8 -*-
# author: kiven

from rest_framework import viewsets
from optasks.models import Project, ProjectEnclosure, ProjectType, DemandManager
from optasks.serializers import (ProjectSerializer,
                                 ProjectEnclosureSerializer,
                                 ProjectTypeSerializer,
                                 DemandManagerSerializer)


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all().order_by('status', '-create_time')
    serializer_class = ProjectSerializer
    filter_fields = ['pid', 'status']
    search_fields = ['name', 'content', 'type__name']
    ordering_fields = ('level', 'task_complete', 'create_time')


class ProjectEnclosureViewSet(viewsets.ModelViewSet):
    queryset = ProjectEnclosure.objects.all()
    serializer_class = ProjectEnclosureSerializer
    filter_fields = ['project__id']


class ProjectTypeViewSet(viewsets.ModelViewSet):
    queryset = ProjectType.objects.all()
    serializer_class = ProjectTypeSerializer


class DemandManagerViewSet(viewsets.ModelViewSet):
    queryset = DemandManager.objects.all().order_by('-create_time')
    serializer_class = DemandManagerSerializer
    search_fields = ['name', 'content']
    ordering_fields = ['status', 'create_time']
    filter_fields = ['status', 'pid', 'create_user__username']
