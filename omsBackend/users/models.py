# -*- coding: utf-8 -*-
# author: kiven

from django.db import models
# from django.contrib.auth.models import Group
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser


class UserManager(BaseUserManager):
    def create_user(self, username, password=None):
        """
        username 是唯一标识，没有会报错
        """

        if not username:
            raise ValueError('Users must have an username')

        user = self.model(
            username=username,
        )
        user.set_password(password)  # 检测密码合理性
        user.save(using=self._db)  # 保存密码
        return user

    def create_superuser(self, username, password):
        user = self.create_user(username=username,
                                password=password,
                                )
        user.is_admin = True  # 比创建用户多的一个字段
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    username = models.CharField(max_length=32, unique=True, db_index=True)
    email = models.EmailField(max_length=255, null=True, blank=True)
    skype = models.CharField(max_length=255, null=True, blank=True)
    groups = models.ManyToManyField('Group', null=True, blank=True, verbose_name=u'部门')
    create_date = models.DateField(auto_now=True, verbose_name=u'创建时间')
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    roles = models.ForeignKey('Role', on_delete=models.SET_NULL, null=True, blank=True, verbose_name=u'角色')

    USERNAME_FIELD = 'username'  # 必须有一个唯一标识--USERNAME_FIELD

    # REQUIRED_FIELDS = ['email']  # 创建superuser时的必须字段

    def __str__(self):  # __unicode__ on Python 2
        return self.username

    @property
    def is_staff(self):
        return self.is_admin

    class Meta:
        verbose_name = u'用户'
        verbose_name_plural = u'用户'

    objects = UserManager()  # 创建用户


class Group(models.Model):
    name = models.CharField(max_length=64, unique=True, verbose_name=u'部门')
    desc = models.CharField(max_length=64, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u'组'
        verbose_name_plural = u'部门'


class Role(models.Model):
    name = models.CharField(max_length=64, unique=True, verbose_name=u'角色')
    desc = models.CharField(max_length=64, null=True, blank=True, verbose_name=u'描述')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u'角色'
        verbose_name_plural = u'角色'
