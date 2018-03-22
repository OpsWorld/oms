# -*- coding: utf-8 -*-
# author: kiven

from rest_framework import viewsets
from optasks.models import OpsProject, OpsDemandManager, OpsDemandEnclosure
from optasks.serializers import (OpsProjectSerializer,
                                 OpsDemandManagerSerializer,
                                 OpsDemandEnclosureSerializer)


class OpsDemandManagerViewSet(viewsets.ModelViewSet):
    queryset = OpsDemandManager.objects.all().order_by('start_time')
    serializer_class = OpsDemandManagerSerializer
    search_fields = ['name', 'pid']
    ordering_fields = ['task_complete', 'start_time', 'status']
    filter_fields = ['status', 'pid', 'create_user__username']


class OpsDemandEnclosureViewSet(viewsets.ModelViewSet):
    queryset = OpsDemandEnclosure.objects.all()
    serializer_class = OpsDemandEnclosureSerializer
    filter_fields = ['project__id']


class OpsProjectViewSet(viewsets.ModelViewSet):
    queryset = OpsProject.objects.all().order_by('start_time')
    serializer_class = OpsProjectSerializer
    filter_fields = ['demand__id']
