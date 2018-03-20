# -*- coding: utf-8 -*-
# author: itimor

from rest_framework import serializers
from jobs.models import Jobs, Deployenv, Deploycmd, DeployJobs, DeployTicket, DeployTicketEnclosure
from hosts.models import Host
from users.models import User
from tools.models import Upload
from omsBackend.settings import sapi


class JobsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Jobs
        fields = ['url', 'id', 'name', 'version', 'content', 'code_url', 'deploy_path', 'cur_step', 'total_step',
                  'done', 'create_time', 'showdev', 'desc']


class DeployenvSerializer(serializers.ModelSerializer):
    deploy_hosts = serializers.SlugRelatedField(many=True, queryset=Host.objects.all(), slug_field='hostname')

    class Meta:
        model = Deployenv
        fields = ['url', 'id', 'job', 'name', 'level', 'deploy_hosts']


class DeploycmdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deploycmd
        fields = ['url', 'id', 'env', 'name', 'deploy_cmd']


class DeployJobsSerializer(serializers.ModelSerializer):
    action_user = serializers.SlugRelatedField(queryset=User.objects.all(), slug_field='username')
    job = serializers.SlugRelatedField(queryset=Jobs.objects.all(), slug_field='name')

    class Meta:
        model = DeployJobs
        fields = ['url', 'id', 'job', 'j_id', 'deploy_status', 'deploy_hosts', 'deploy_cmd_host', 'version', 'content',
                  'env', 'deploy_path', 'deploy_cmd', 'action_user', 'result', 'create_time']

    def create(self, validated_data):
        deploy_path = validated_data["deploy_path"]
        deploy_cmds = validated_data["deploy_cmd"]
        deploy_hosts = validated_data["deploy_hosts"]
        version = validated_data["version"]
        env_id = validated_data["env"]
        env_name = Deployenv.objects.get(id=env_id).name
        print(env_name)
        jids = []
        for cmd in deploy_cmds.split('||'):
            import re
            deploy_cmd = Deploycmd.objects.get(env=env_id, name=cmd).deploy_cmd
            print(deploy_cmd)
            if env_name == 'svn':
                print('svn发布')
                deploy_cmd = re.sub(r'\$\w+', deploy_path, deploy_cmd) + ' -r ' + version

            jid = sapi.remote_cmd(tgt=deploy_hosts.split(','), arg=deploy_cmd)
            validated_data["j_id"] = jid
            jids.append(jid)
            validated_data["env"] = env_name
            validated_data["deploy_cmd_host"] = cmd
            deployjob = DeployJobs.objects.create(**validated_data)
            deployjob.save()
        return {"jids": jids}


class DeployTicketSerializer(serializers.ModelSerializer):
    create_user = serializers.SlugRelatedField(queryset=User.objects.all(), slug_field='username')

    class Meta:
        model = DeployTicket
        fields = ['url', 'id', 'name', 'create_user', 'version', 'content', 'status', 'skype_to', 'create_time']


class DeployTicketEnclosureSerializer(serializers.ModelSerializer):
    create_user = serializers.SlugRelatedField(queryset=User.objects.all(), slug_field='username')
    file = serializers.SlugRelatedField(queryset=Upload.objects.all(), slug_field='filepath')

    class Meta:
        model = DeployTicketEnclosure
        fields = ('url', 'id', 'ticket', 'file', 'create_user', 'create_time')
