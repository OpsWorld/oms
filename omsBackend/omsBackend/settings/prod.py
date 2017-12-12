# -*- coding: utf-8 -*-
# author: itimor

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'django_filters',  # 过滤
    'corsheaders',  # 跨域
    'django_python3_ldap',  # ldap认证
    'dry_rest_permissions',  # 权限
    'channels',   #djanog异步通信
    'worktickets',
    'tools',
    'users',
    'menus',
    'perms',
]

DATABASES = {
   'default': {
       'ENGINE': 'django.db.backends.postgresql_psycopg2',
       'NAME': 'oms',
       'USER': 'oms',
       'PASSWORD': '123456',
       'HOST': '127.0.0.1',
       'PORT': '5432'
   }
}

#使用ldap认证
AUTHENTICATION_BACKENDS = ("django_python3_ldap.auth.LDAPBackend",)
LDAP_AUTH_URL = "ldap://192.168.6.101:389"
LDAP_AUTH_SEARCH_BASE = "ou=AllUser,dc=tb-gaming,dc=local"
LDAP_AUTH_CONNECTION_USERNAME = r'tb-gaming\itconfig'
LDAP_AUTH_CONNECTION_PASSWORD = r'TUjweiAHZQ'