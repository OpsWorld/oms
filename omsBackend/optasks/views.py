# -*- coding: utf-8 -*-
# author: kiven

from rest_framework import viewsets
from optasks.models import OpsProject, OpsDemandManager, OpsDemandEnclosure
from optasks.serializers import (OpsProjectSerializer,
                                 OpsDemandManagerSerializer,
                                 OpsDemandEnclosureSerializer)


class OpsProjectViewSet(viewsets.ModelViewSet):
    queryset = OpsProject.objects.all().order_by('status', '-create_time')
    serializer_class = OpsProjectSerializer
    filter_fields = ['pid', 'status', 'demand__id']
    search_fields = ['pid', 'name', 'content']
    ordering_fields = ['task_complete', 'create_time']


class OpsDemandManagerViewSet(viewsets.ModelViewSet):
    queryset = OpsDemandManager.objects.all().order_by('-create_time')
    serializer_class = OpsDemandManagerSerializer
    search_fields = ['name', 'content']
    ordering_fields = ['status', 'create_time']
    filter_fields = ['status', 'pid', 'create_user__username']


class OpsDemandEnclosureViewSet(viewsets.ModelViewSet):
    queryset = OpsDemandEnclosure.objects.all()
    serializer_class = OpsDemandEnclosureSerializer
    filter_fields = ['project__id']