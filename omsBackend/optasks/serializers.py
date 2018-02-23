# -*- coding: utf-8 -*-
# author: kiven

from optasks.models import Project, ProjectEnclosure, ProjectType, DemandManager
from rest_framework import serializers
from users.models import User, Group
from tools.models import Upload


class ProjectSerializer(serializers.ModelSerializer):
    type = serializers.SlugRelatedField(queryset=ProjectType.objects.all(), slug_field='name', allow_null=True)
    create_user = serializers.SlugRelatedField(queryset=User.objects.all(), slug_field='username')
    action_user = serializers.SlugRelatedField(queryset=User.objects.all(), slug_field='username')

    class Meta:
        model = Project
        fields = (
            'url', 'id', 'pid', 'name', 'type', 'level', 'status', 'task_complete', 'content', 'create_user',
            'action_user', 'create_time', 'update_time', 'start_time', 'end_time')


class ProjectEnclosureSerializer(serializers.ModelSerializer):
    create_user = serializers.SlugRelatedField(queryset=User.objects.all(), slug_field='username')
    file = serializers.SlugRelatedField(queryset=Upload.objects.all(), slug_field='filepath')

    class Meta:
        model = ProjectEnclosure
        fields = ('url', 'id', 'project', 'file', 'create_user', 'create_time')


class ProjectTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectType
        fields = ('url', 'id', 'name', 'desc')


class DemandManagerSerializer(serializers.ModelSerializer):
    type = serializers.SlugRelatedField(queryset=ProjectType.objects.all(), slug_field='name', allow_null=True)
    create_user = serializers.SlugRelatedField(queryset=User.objects.all(), slug_field='username')

    class Meta:
        model = DemandManager
        fields = (
            'url', 'id', 'pid', 'name', 'type', 'content', 'create_user', 'status', 'create_time', 'end_time')
