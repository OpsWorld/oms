# -*- coding: utf-8 -*-
# author: itimor

from rest_framework import serializers
from jobs.models import Jobs, Deployenv, DeployJobs
from hosts.models import Host


class JobsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Jobs
        fields = ['url', 'id', 'name', 'code_repo', 'code_url', 'create_time', 'update_time', 'desc']


class DeployenvSerializer(serializers.ModelSerializer):
    job = serializers.SlugRelatedField(queryset=Jobs.objects.all(), slug_field='name')
    hosts = serializers.SlugRelatedField(many=True, queryset=Host.objects.all(), slug_field='hostname')

    class Meta:
        model = Deployenv
        fields = ['url', 'id', 'job', 'name', 'path', 'hosts', 'desc']


class DeployJobsSerializer(serializers.ModelSerializer):
    job = serializers.SlugRelatedField(queryset=Jobs.objects.all(), slug_field='name')
    action_user = serializers.SlugRelatedField(queryset=Jobs.objects.all(), slug_field='username')

    class Meta:
        model = DeployJobs
        fields = ['url', 'id', 'job', 'j_id', 'deploy_status', 'hosts', 'env', 'version', 'action_user', 'result',
                  'create_time']
