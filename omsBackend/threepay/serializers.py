# -*- coding: utf-8 -*-
# author: kiven

from threepay.models import (Platform, Merchant, ThreePayEnclosure, PayChannelName, PayChannel, ThreePayComment,
                             PlatformPayChannel)
from rest_framework import serializers
from users.models import User, Group
from tools.models import Upload


class PlatformSerializer(serializers.ModelSerializer):
    class Meta:
        model = Platform
        fields = ('url', 'id', 'name', 'ipaddr', 'desc')


class MerchantSerializer(serializers.ModelSerializer):
    platform = serializers.SlugRelatedField(queryset=Platform.objects.all(), slug_field='name')

    class Meta:
        model = Merchant
        fields = (
            'url', 'id', 'platform', 'name', 'm_id', 'domain', 'three')


class PayChannelNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = PayChannelName
        fields = ('url', 'id', 'name', 'desc')


class PayChannelSerializer(serializers.ModelSerializer):
    platform = serializers.SlugRelatedField(queryset=Platform.objects.all(), slug_field='name')
    merchant = serializers.SlugRelatedField(queryset=Merchant.objects.all(), slug_field='name')
    type = serializers.SlugRelatedField(queryset=PayChannelName.objects.all(), slug_field='name')
    create_user = serializers.SlugRelatedField(queryset=User.objects.all(), slug_field='username')
    action_user = serializers.SlugRelatedField(queryset=User.objects.all(), slug_field='username')

    class Meta:
        model = PayChannel
        fields = (
            'url', 'id', 'name', 'platform', 'merchant', 'type', 'rate', 'keyinfo', 'm_forwardurl', 'm_submiturl',
            'create_user', 'action_user', 'create_time')

    def create(self, validated_data):
        platform = validated_data["platform"]
        type = validated_data["type"]
        create_user = validated_data["create_user"]
        name = '{}-{}'.format(platform, type)
        try:
            platformpaychannel = PlatformPayChannel.objects.get(name=name)
        except:
            import datetime
            pid = 'tp' + datetime.datetime.now().strftime('%Y%m%d%H%M%S')
            platformpaychannel = PlatformPayChannel.objects.create(pid=pid,
                                                                   name=name,
                                                                   platform=platform,
                                                                   type=type,
                                                                   create_user=create_user)
            platformpaychannel.save()
        paychannel = PayChannel.objects.create(**validated_data)
        paychannel.save()
        return paychannel


class ThreePayEnclosureSerializer(serializers.ModelSerializer):
    ticket = serializers.SlugRelatedField(queryset=Platform.objects.all(), slug_field='name')
    create_user = serializers.SlugRelatedField(queryset=User.objects.all(), slug_field='username')
    file = serializers.SlugRelatedField(queryset=Upload.objects.all(), slug_field='filepath')

    class Meta:
        model = ThreePayEnclosure
        fields = ('url', 'id', 'ticket', 'file', 'create_user', 'create_time')


class ThreePayCommentSerializer(serializers.ModelSerializer):
    create_user = serializers.SlugRelatedField(queryset=User.objects.all(), slug_field='username')
    merchant = serializers.SlugRelatedField(queryset=Merchant.objects.all(), slug_field='name')

    class Meta:
        model = ThreePayComment
        fields = ('url', 'id', 'ticket', 'merchant', 'content', 'create_user', 'create_time')


class PlatformPayChannelSerializer(serializers.ModelSerializer):
    platform = serializers.SlugRelatedField(queryset=Platform.objects.all(), slug_field='name')
    type = serializers.SlugRelatedField(queryset=PayChannelName.objects.all(), slug_field='name')
    create_user = serializers.SlugRelatedField(queryset=User.objects.all(), slug_field='username')

    class Meta:
        model = PlatformPayChannel
        fields = ('url', 'id', 'pid', 'name', 'platform', 'type', 'level', 'status', 'create_user', 'create_time')
