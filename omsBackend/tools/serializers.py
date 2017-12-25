# -*- coding: utf-8 -*-
# author: itimor

from rest_framework import serializers
from tools.models import Upload, Sendmail, Sendmessage
from users.models import User


class UploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Upload
        fields = ['url', 'id', 'username', 'file', 'filename', 'filepath', 'archive', 'type', 'size', 'create_time']


class SendmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sendmail
        fields = ['url', 'id', 'to', 'cc', 'sub', 'content', 'create_time']


class SendmessageSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(queryset=User.objects.all(), slug_field='username')

    class Meta:
        model = Sendmessage
        fields = ['url', 'id', 'user', 'title', 'message', 'is_html', 'duration', 'state']
