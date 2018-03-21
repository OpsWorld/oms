# -*- coding: utf-8 -*-
# author: kiven

from optasks.models import OpsProject, OpsDemandManager, OpsDemandEnclosure
from rest_framework import serializers
from users.models import User, Group
from tools.models import Upload


class OpsDemandManagerSerializer(serializers.ModelSerializer):
    create_user = serializers.SlugRelatedField(queryset=User.objects.all(), slug_field='username')

    class Meta:
        model = OpsDemandManager
        fields = (
            'url', 'id', 'pid', 'name', 'task_complete', 'content', 'create_user', 'status', 'create_time',
            'start_time', 'end_time')


class OpsDemandEnclosureSerializer(serializers.ModelSerializer):
    create_user = serializers.SlugRelatedField(queryset=User.objects.all(), slug_field='username')
    file = serializers.SlugRelatedField(queryset=Upload.objects.all(), slug_field='filepath')

    class Meta:
        model = OpsDemandEnclosure
        fields = ('url', 'id', 'project', 'file', 'create_user', 'create_time')


class OpsProjectSerializer(serializers.ModelSerializer):
    create_user = serializers.SlugRelatedField(queryset=User.objects.all(), slug_field='username')
    action_user = serializers.SlugRelatedField(queryset=User.objects.all(), slug_field='username')

    class Meta:
        model = OpsProject
        fields = (
            'url', 'id', 'demand', 'pid', 'name', 'status', 'task_complete', 'content', 'create_user', 'action_user',
            'create_time', 'start_time', 'end_time')
