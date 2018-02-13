# -*- coding: utf-8 -*-
# author: kiven

from rest_framework import viewsets
from projects.models import Project, ProjectComment, ProjectType, BugManager, TestManager
from projects.serializers import (ProjectSerializer,
                                  ProjectCommentSerializer,
                                  ProjectTypeSerializer,
                                  BugManagerSerializer,
                                  TestManagerSerializer)


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all().order_by('create_time')
    serializer_class = ProjectSerializer


class ProjectCommentViewSet(viewsets.ModelViewSet):
    queryset = ProjectComment.objects.all().order_by('create_time')
    serializer_class = ProjectCommentSerializer


class ProjectTypeViewSet(viewsets.ModelViewSet):
    queryset = ProjectType.objects.all()
    serializer_class = ProjectTypeSerializer


class BugManagerViewSet(viewsets.ModelViewSet):
    queryset = BugManager.objects.all()
    serializer_class = BugManagerSerializer


class TestManagerViewSet(viewsets.ModelViewSet):
    queryset = TestManager.objects.all()
    serializer_class = TestManagerSerializer
