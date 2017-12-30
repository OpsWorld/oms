# -*- coding: utf-8 -*-
# author: kiven

from worktickets.models import WorkTicket, TicketComment, TicketEnclosure, TicketType, TicketWiki
from rest_framework import serializers
from users.models import User, Group
from tools.models import Upload


class WorkTicketSerializer(serializers.ModelSerializer):
    type = serializers.SlugRelatedField(queryset=TicketType.objects.all(), slug_field='name', allow_null=True)
    create_user = serializers.SlugRelatedField(queryset=User.objects.all(), slug_field='username')
    action_user = serializers.SlugRelatedField(queryset=User.objects.all(), slug_field='username')
    edit_user = serializers.SlugRelatedField(queryset=User.objects.all(), slug_field='username', allow_null=True)
    follower = serializers.SlugRelatedField(many=True, queryset=User.objects.all(), slug_field='username',allow_null=True)
    create_group = serializers.SlugRelatedField(many=True, queryset=Group.objects.all(), slug_field='name',allow_null=True)

    class Meta:
        model = WorkTicket
        fields = (
            'url', 'id', 'ticketid', 'title', 'type', 'content', 'create_user', 'action_user', 'edit_user', 'follower',
            'create_group', 'level', 'ticket_status', 'create_time', 'update_time', 'action_time', 'end_time',
            'cost_time')
        read_only_fields = ('cost_time',)


class TicketCommentSerializer(serializers.ModelSerializer):
    create_user = serializers.SlugRelatedField(queryset=User.objects.all(), slug_field='username')

    class Meta:
        model = TicketComment
        fields = ('url', 'id', 'ticket', 'content', 'create_user', 'create_time')


class TicketEnclosureSerializer(serializers.ModelSerializer):
    create_user = serializers.SlugRelatedField(queryset=User.objects.all(), slug_field='username')
    file = serializers.SlugRelatedField(queryset=Upload.objects.all(), slug_field='filepath')

    class Meta:
        model = TicketEnclosure
        fields = ('url', 'id', 'ticket', 'file', 'create_user', 'create_time')


class TicketTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketType
        fields = ('url', 'id', 'name', 'desc')


class TicketWikiSerializer(serializers.ModelSerializer):
    create_user = serializers.SlugRelatedField(queryset=User.objects.all(), slug_field='username')

    class Meta:
        model = TicketWiki
        fields = ('url', 'id', 'title', 'type', 'content', 'create_user', 'create_time')

