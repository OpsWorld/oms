# -*- coding: utf-8 -*-
# author: itimor

from rest_framework import serializers
from jobs.models import Jobs, Deployenv
from hosts.models import Host


class JobsSerializer(serializers.ModelSerializer):
    hosts = serializers.SlugRelatedField(many=True, queryset=Host.objects.all(), slug_field='hostname')

    class Meta:
        model = Jobs
        fields = ['url', 'id', 'name', 'hosts', 'code_repo', 'code_url', 'deploy_script', 'deploy_status',
                  'create_time', 'update_time', 'desc']


class DeployenvSerializer(serializers.ModelSerializer):
    job = serializers.SlugRelatedField(queryset=Jobs.objects.all(), slug_field='name')

    class Meta:
        model = Deployenv
        fields = ['url', 'id', 'job', 'name', 'path', 'desc']
