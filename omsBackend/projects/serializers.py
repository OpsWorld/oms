# -*- coding: utf-8 -*-
# author: kiven

from projects.models import Project, ProjectComment, ProjectType
from rest_framework import serializers
from users.models import User, Group


class ProjectSerializer(serializers.ModelSerializer):
    type = serializers.SlugRelatedField(queryset=ProjectType.objects.all(), slug_field='name', allow_null=True)
    create_user = serializers.SlugRelatedField(queryset=User.objects.all(), slug_field='username')
    action_user = serializers.SlugRelatedField(many=True, queryset=User.objects.all(), slug_field='username',
                                               allow_null=True)
    follow_user = serializers.SlugRelatedField(many=True, queryset=User.objects.all(), slug_field='username',
                                               allow_null=True)

    class Meta:
        model = Project
        fields = (
            'url', 'id', 'pid', 'title', 'type', 'level', 'status', 'task_complete', 'test_complete', 'content',
            'create_user', 'action_user', 'follow_user', 'from_user', 'create_time', 'update_time', 'start_time',
            'desc')


class ProjectCommentSerializer(serializers.ModelSerializer):
    create_user = serializers.SlugRelatedField(queryset=User.objects.all(), slug_field='username')

    class Meta:
        model = ProjectComment
        fields = ('url', 'id', 'ticket', 'content', 'create_user', 'create_time')


class ProjectTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectType
        fields = ('url', 'id', 'name', 'desc')
