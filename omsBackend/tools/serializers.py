# -*- coding: utf-8 -*-
# author: itimor

from rest_framework import serializers
from tools.models import Upload, Sendmail


class UploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Upload
        fields = ['url', 'id', 'username', 'file', 'filename', 'filepath', 'archive', 'type', 'size', 'create_time']


class SendmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Upload
        fields = ['url', 'id', 'to', 'cc', 'sub', 'content', 'create_time']