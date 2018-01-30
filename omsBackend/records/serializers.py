# -*- coding: utf-8 -*-
# author: itimor

from rest_framework import serializers
from records.models import Record


class RecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Record
        fields = ['url', 'id', 'name', 'type', 'asset', 'method', 'before', 'after', 'create_user', 'create_time']
