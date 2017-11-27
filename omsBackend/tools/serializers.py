# -*- coding: utf-8 -*-
# author: itimor

from rest_framework import serializers
from tools.models import Duty, Upload


class UploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Upload
        fields = ['url', 'id', 'username', 'file', 'filename', 'filepath', 'archive', 'type', 'size', 'create_time']


class DutySerializer(serializers.ModelSerializer):
    images = serializers.SlugRelatedField(many=True, queryset=Upload.objects.all(), slug_field='filepath')
    class Meta:
        model = Duty
        fields = ['url', 'id', 'username', 'shift', 'content', 'images', 'create_time']
        read_only_fields = ('create_time', )