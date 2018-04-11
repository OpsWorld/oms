# -*- coding: utf-8 -*-
# author: kiven

from .models import ZkUser, Punch, PunchSet
from rest_framework import serializers


class ZkUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = ZkUser
        fields = ('url', 'user_id', 'username', 'password', 'role', 'is_active')


class PunchSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(queryset=ZkUser.objects.all(), slug_field='username')

    class Meta:
        model = Punch
        fields = (
            'url', 'id', 'user', 'verifymode', 'swork_status', 'ework_status', 'nowork_status', 'create_date',
            'swork_time', 'ework_time', 'swork_timec', 'ework_timec', 'work_time')


class PunchSetSerializer(serializers.ModelSerializer):
    class Meta:
        model = PunchSet
        fields = ('url', 'id', 'swork_time', 'ework_time', 'swork_stime', 'swork_etime', 'ework_stime', 'ework_etime')
