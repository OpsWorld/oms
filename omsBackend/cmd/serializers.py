# -*- coding: utf-8 -*-
# author: itimor

from rest_framework import serializers
from cmd.models import Cmdrun
from users.models import User


class CmdrunSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(queryset=User.objects.all(), slug_field='username')
    class Meta:
        model = Cmdrun
        fields = ['url', 'id', 'user', 'hosts', 'cmd']