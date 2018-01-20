# -*- coding: utf-8 -*-
# author: itimor

from rest_framework import serializers
from tools.models import Upload, Sendmail, Sendmessage, Calender


class UploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Upload
        fields = ['url', 'id', 'username', 'file', 'filename', 'filepath', 'archive', 'type', 'size', 'create_time']


class SendmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sendmail
        fields = ['url', 'id', 'to', 'cc', 'sub', 'content', 'create_time']


class SendmessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sendmessage
        fields = ['url', 'id', 'action_user', 'title', 'message']

class CalenderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Calender
        fields = ['url', 'id', 'title', 'start', 'end','content', 'cssClass']