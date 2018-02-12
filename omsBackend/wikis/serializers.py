# -*- coding: utf-8 -*-
# author: kiven

from wikis.models import Wiki, OpsWiki
from rest_framework import serializers
from users.models import User, Group
from worktickets.models import TicketType


class WikiSerializer(serializers.ModelSerializer):
    create_user = serializers.SlugRelatedField(queryset=User.objects.all(), slug_field='username')
    type = serializers.SlugRelatedField(queryset=TicketType.objects.all(), slug_field='name', allow_null=True)

    class Meta:
        model = Wiki
        fields = ('url', 'id', 'title', 'type', 'content', 'create_user', 'create_time', 'update_time')


class OpsWikiSerializer(serializers.ModelSerializer):
    create_user = serializers.SlugRelatedField(queryset=User.objects.all(), slug_field='username')

    class Meta:
        model = OpsWiki
        fields = ('url', 'id', 'title', 'content', 'create_user', 'create_time', 'update_time')