# -*- coding: utf-8 -*-
# author: itimor

from rest_framework import serializers
from jobs.models import Jobs, Deployenv, Deploycmd, DeployJobs, DeployVersion, DeployTicket, DeployTicketEnclosure
from hosts.models import Host
from users.models import User
from tools.models import Upload
from omsBackend.settings import sapi


class JobsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Jobs
        fields = ['url', 'id', 'name', 'code_url', 'deploy_path', 'cur_step', 'create_time', 'showdev', 'desc']


class DeployenvSerializer(serializers.ModelSerializer):
    deploy_hosts = serializers.SlugRelatedField(many=True, queryset=Host.objects.all(), slug_field='hostname')

    class Meta:
        model = Deployenv
        fields = ['url', 'id', 'job', 'name', 'deploy_hosts']


class DeploycmdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deploycmd
        fields = ['url', 'id', 'env', 'name', 'deploy_cmd']


class DeployJobsSerializer(serializers.ModelSerializer):
    action_user = serializers.SlugRelatedField(queryset=User.objects.all(), slug_field='username')
    job = serializers.SlugRelatedField(queryset=Jobs.objects.all(), slug_field='name')

    class Meta:
        model = DeployJobs
        fields = ['url', 'id', 'job', 'j_id', 'deploy_status', 'deploy_hosts', 'version', 'content', 'env', 'deploy_cmd', 'action_user', 'result', 'create_time']

    def create(self, validated_data):
        deploy_cmd = validated_data["deploy_cmd"]
        deploy_hosts = validated_data["deploy_hosts"]
        print(deploy_cmd)
        jid = sapi.remote_cmd(tgt=deploy_hosts.split(','), fun='cmd.run', arg=deploy_cmd)
        validated_data["j_id"] = jid
        deployjob = DeployJobs.objects.create(**validated_data)
        deployjob.save()
        return deployjob


class DeployVersionSerializer(serializers.ModelSerializer):
    job = serializers.SlugRelatedField(queryset=Jobs.objects.all(), slug_field='name')

    class Meta:
        model = DeployVersion
        fields = ['url', 'id', 'job', 'version', 'content']


class DeployTicketSerializer(serializers.ModelSerializer):
    create_user = serializers.SlugRelatedField(queryset=User.objects.all(), slug_field='username')

    class Meta:
        model = DeployTicket
        fields = ['url', 'id', 'name', 'create_user', 'version', 'content', 'status', 'create_time']


class DeployTicketEnclosureSerializer(serializers.ModelSerializer):
    create_user = serializers.SlugRelatedField(queryset=User.objects.all(), slug_field='username')
    file = serializers.SlugRelatedField(queryset=Upload.objects.all(), slug_field='filepath')

    class Meta:
        model = DeployTicketEnclosure
        fields = ('url', 'id', 'ticket', 'file', 'create_user', 'create_time')