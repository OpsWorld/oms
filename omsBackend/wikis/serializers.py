# -*- coding: utf-8 -*-
# author: kiven

from wikis.models import Wiki
from rest_framework import serializers
from users.models import User, Group
from worktickets.models import TicketType


class WikiSerializer(serializers.ModelSerializer):
    create_user = serializers.SlugRelatedField(queryset=User.objects.all(), slug_field='username')
    create_group = serializers.SlugRelatedField(many=True, queryset=Group.objects.all(), slug_field='name', allow_null=True)
    type = serializers.SlugRelatedField(queryset=TicketType.objects.all(), slug_field='name', allow_null=True)

    class Meta:
        model = Wiki
        fields = ('url', 'id', 'title', 'type', 'content', 'create_user', 'create_group', 'create_time', 'update_time')
