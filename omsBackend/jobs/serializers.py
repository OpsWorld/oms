# -*- coding: utf-8 -*-
# author: itimor

from rest_framework import serializers
from jobs.models import Jobs, Deployenv, DeployJobs
from hosts.models import Host
from users.models import User
from omsBackend.settings import sapi


class JobsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Jobs
        fields = ['url', 'id', 'name', 'code_repo', 'code_url', 'create_time', 'desc']


class DeployenvSerializer(serializers.ModelSerializer):
    job = serializers.SlugRelatedField(queryset=Jobs.objects.all(), slug_field='name')
    hosts = serializers.SlugRelatedField(many=True, queryset=Host.objects.all(), slug_field='hostname')

    class Meta:
        model = Deployenv
        fields = ['url', 'id', 'job', 'name', 'path', 'hosts', 'desc']


class DeployJobsSerializer(serializers.ModelSerializer):
    job = serializers.SlugRelatedField(queryset=Jobs.objects.all(), slug_field='name')
    action_user = serializers.SlugRelatedField(queryset=User.objects.all(), slug_field='username')

    class Meta:
        model = DeployJobs
        fields = ['url', 'id', 'job', 'j_id', 'deploy_status', 'hosts', 'env', 'version', 'deploy_path', 'action_user',
                  'result', 'create_time']

    def create(self, validated_data):
        hosts = validated_data["hosts"]
        version = validated_data["version"]
        deploy_path = validated_data["deploy_path"]
        runcmd = 'cd %s;svn up -r %s' % (deploy_path,version)
        cmd = "echo '发布版本：'%s; echo '发布路径：'%s; echo '发布命令：%s'" % (version, deploy_path, runcmd)
        print(cmd)
        jid = sapi.remote_cmd(tgt=hosts, fun='cmd.run', arg=cmd)
        validated_data["j_id"] = jid
        deployjob = DeployJobs.objects.create(**validated_data)
        deployjob.save()
        return deployjob