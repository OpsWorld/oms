# -*- coding: utf-8 -*-
# author: kiven

from rest_framework import viewsets
from optasks.models import OpsProject, OpsProjectEnclosure, OpsProjectType, OpsDemandManager
from optasks.serializers import (OpsProjectSerializer,
                                 OpsProjectEnclosureSerializer,
                                 OpsProjectTypeSerializer,
                                 OpsDemandManagerSerializer)


class OpsProjectViewSet(viewsets.ModelViewSet):
    queryset = OpsProject.objects.all().order_by('status', '-create_time')
    serializer_class = OpsProjectSerializer
    filter_fields = ['pid', 'status']
    search_fields = ['name', 'content', 'type__name']
    ordering_fields = ('level', 'task_complete', 'create_time')


class OpsProjectEnclosureViewSet(viewsets.ModelViewSet):
    queryset = OpsProjectEnclosure.objects.all()
    serializer_class = OpsProjectEnclosureSerializer
    filter_fields = ['project__id']


class OpsProjectTypeViewSet(viewsets.ModelViewSet):
    queryset = OpsProjectType.objects.all()
    serializer_class = OpsProjectTypeSerializer


class OpsDemandManagerViewSet(viewsets.ModelViewSet):
    queryset = OpsDemandManager.objects.all().order_by('-create_time')
    serializer_class = OpsDemandManagerSerializer
    search_fields = ['name', 'content']
    ordering_fields = ['status', 'create_time']
    filter_fields = ['status', 'pid', 'create_user__username']
