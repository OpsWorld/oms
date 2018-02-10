# -*- coding: utf-8 -*-
# author: kiven

from rest_framework import viewsets
from projects.models import Project, ProjectComment, ProjectType
from projects.serializers import (ProjectSerializer,
                                  ProjectCommentSerializer,
                                  ProjectTypeSerializer)


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all().order_by('create_time')
    serializer_class = ProjectSerializer


class ProjectCommentViewSet(viewsets.ModelViewSet):
    queryset = ProjectComment.objects.all().order_by('create_time')
    serializer_class = ProjectCommentSerializer


class ProjectTypeViewSet(viewsets.ModelViewSet):
    queryset = ProjectType.objects.all()
    serializer_class = ProjectTypeSerializer
