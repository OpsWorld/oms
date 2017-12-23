# -*- coding: utf-8 -*-
# author: kiven

from threepay.models import Platform, Merchant, ThreePayEnclosure, PayChannelName, PayChannel
from rest_framework import serializers
from users.models import User, Group
from tools.models import Upload


class PlatformSerializer(serializers.ModelSerializer):
    class Meta:
        model = Platform
        fields = ('url', 'id', 'name', 'desc')


class MerchantSerializer(serializers.ModelSerializer):
    platform = serializers.SlugRelatedField(queryset=Platform.objects.all(), slug_field='name')

    class Meta:
        model = Merchant
        fields = (
            'url', 'id', 'platform', 'name', 'm_id', 'three')


class PayChannelNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = PayChannelName
        fields = ('url', 'id', 'name', 'desc')


class PayChannelSerializer(serializers.ModelSerializer):
    platform = serializers.SlugRelatedField(queryset=Platform.objects.all(), slug_field='name')
    merchant = serializers.SlugRelatedField(queryset=Merchant.objects.all(), slug_field='name')
    type = serializers.SlugRelatedField(queryset=PayChannelName.objects.all(), slug_field='name')
    action_user = serializers.SlugRelatedField(queryset=User.objects.all(), slug_field='username')
    class Meta:
        model = PayChannel
        fields = (
            'url', 'id', 'platform', 'merchant', 'type', 'm_md5key', 'm_public_key', 'm_private_key', 'p_public_key',
            'm_forwardurl', 'm_submiturl', 'm_backurl', 'level','status','action_user','create_time')


class ThreePayEnclosureSerializer(serializers.ModelSerializer):
    create_user = serializers.SlugRelatedField(queryset=User.objects.all(), slug_field='username')
    file = serializers.SlugRelatedField(queryset=Upload.objects.all(), slug_field='filepath')

    class Meta:
        model = ThreePayEnclosure
        fields = ('url', 'id', 'ticket', 'file', 'create_user', 'create_time')
