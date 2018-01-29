# -*- coding: utf-8 -*-
# author: kiven

from users.models import User, Role, Group
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    groups = serializers.SlugRelatedField(many=True, queryset=Group.objects.all(), slug_field='name', allow_null=True)
    roles = serializers.SlugRelatedField(queryset=Role.objects.all(), slug_field='name', allow_null=True)

    class Meta:
        model = User
        fields = ('url', 'id', 'username', 'email', 'skype', 'groups', 'is_active', 'roles', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        groups = validated_data.pop('groups')
        user = User.objects.create(**validated_data)
        user.groups = groups
        try:
            user.set_password(validated_data['password'])
        except:
            pass
        user.save()
        return user

    def update(self, instance, validated_data):
        groups = validated_data.pop('groups')
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.skype = validated_data.get('skype', instance.skype)
        instance.roles = validated_data.get('roles', instance.roles)
        instance.is_active = validated_data.get('is_active', instance.is_active)
        try:
            instance.set_password(validated_data['password'])
        except Exception as e:
            pass
        instance.groups = groups
        instance.save()
        return instance


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'id', 'name', 'desc')


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ('url', 'id', 'name', 'desc')
