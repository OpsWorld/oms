# -*- coding: utf-8 -*-
# author: kiven

from optasks.models import OpsProject, OpsProjectEnclosure, OpsProjectType, OpsDemandManager, OpsDemandEnclosure
from rest_framework import serializers
from users.models import User, Group
from tools.models import Upload


class OpsProjectSerializer(serializers.ModelSerializer):
    type = serializers.SlugRelatedField(queryset=OpsProjectType.objects.all(), slug_field='name', allow_null=True)
    create_user = serializers.SlugRelatedField(queryset=User.objects.all(), slug_field='username')
    action_user = serializers.SlugRelatedField(queryset=User.objects.all(), slug_field='username')

    class Meta:
        model = OpsProject
        fields = (
            'url', 'id', 'pid', 'name', 'type', 'level', 'status', 'task_complete', 'content', 'create_user',
            'action_user', 'create_time', 'update_time', 'start_time', 'end_time')


class OpsProjectEnclosureSerializer(serializers.ModelSerializer):
    create_user = serializers.SlugRelatedField(queryset=User.objects.all(), slug_field='username')
    file = serializers.SlugRelatedField(queryset=Upload.objects.all(), slug_field='filepath')

    class Meta:
        model = OpsProjectEnclosure
        fields = ('url', 'id', 'project', 'file', 'create_user', 'create_time')


class OpsProjectTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = OpsProjectType
        fields = ('url', 'id', 'name', 'desc')


class OpsDemandManagerSerializer(serializers.ModelSerializer):
    type = serializers.SlugRelatedField(queryset=OpsProjectType.objects.all(), slug_field='name', allow_null=True)
    create_user = serializers.SlugRelatedField(queryset=User.objects.all(), slug_field='username')

    class Meta:
        model = OpsDemandManager
        fields = (
            'url', 'id', 'pid', 'name', 'type', 'content', 'create_user', 'status', 'create_time', 'end_time')


class OpsDemandEnclosureSerializer(serializers.ModelSerializer):
    create_user = serializers.SlugRelatedField(queryset=User.objects.all(), slug_field='username')
    file = serializers.SlugRelatedField(queryset=Upload.objects.all(), slug_field='filepath')

    class Meta:
        model = OpsDemandEnclosure
        fields = ('url', 'id', 'project', 'file', 'create_user', 'create_time')