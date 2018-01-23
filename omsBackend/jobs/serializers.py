# -*- coding: utf-8 -*-
# author: itimor

from rest_framework import serializers
from jobs.models import Jobs, DeployJobs
from hosts.models import Host
from users.models import User
from omsBackend.settings import sapi


class JobsSerializer(serializers.ModelSerializer):
    deploy_hosts = serializers.SlugRelatedField(many=True, queryset=Host.objects.all(), slug_field='hostname')

    class Meta:
        model = Jobs
        fields = ['url', 'id', 'name', 'code_repo', 'code_url', 'deploy_hosts', 'deploy_path', 'create_time', 'showdev', 'desc']


# class DeployenvSerializer(serializers.ModelSerializer):
#     job = serializers.SlugRelatedField(queryset=Jobs.objects.all(), slug_field='name')
#     hosts = serializers.SlugRelatedField(many=True, queryset=Host.objects.all(), slug_field='hostname')
#
#     class Meta:
#         model = Deployenv
#         fields = ['url', 'id', 'job', 'name', 'path', 'hosts', 'desc']


class DeployJobsSerializer(serializers.ModelSerializer):
    job = serializers.SlugRelatedField(queryset=Jobs.objects.all(), slug_field='name')
    action_user = serializers.SlugRelatedField(queryset=User.objects.all(), slug_field='username')

    class Meta:
        model = DeployJobs
        fields = ['url', 'id', 'job', 'j_id', 'deploy_status', 'deploy_hosts', 'env', 'version', 'deploy_path', 'content',
                  'action_user', 'result', 'create_time']

    def create(self, validated_data):
        deploy_hosts = validated_data["deploy_hosts"]
        version = validated_data["version"]
        deploy_path = validated_data["deploy_path"]
        print(deploy_path)
        svn_cmd = '"C:/Program Files/TortoiseSVN/bin/svn.exe"'
        runcmd = '{} update {} -r {} --non-interactive --trust-server-cert'.format(svn_cmd,deploy_path, version)
        print(runcmd)
        printcmd = "echo '发布版本：'%s; echo '发布路径：'%s; echo '发布命令：%s'" % (version, deploy_path, runcmd)
        jid = sapi.remote_cmd(tgt=deploy_hosts.split(','), fun='cmd.run', arg=runcmd)
        validated_data["j_id"] = jid
        deployjob = DeployJobs.objects.create(**validated_data)
        deployjob.save()
        return deployjob
