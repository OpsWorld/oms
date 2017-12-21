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
    'worktickets',
    'tools',
    'users',
    'menus',
    'perms',
    'cmd',
    'threepay',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, '../omsBackend.db'),
    }
}

# 使用ldap认证
#AUTHENTICATION_BACKENDS = ("django_python3_ldap.auth.LDAPBackend",)
LDAP_AUTH_URL = "ldap://1.1.1.100:389"
LDAP_AUTH_SEARCH_BASE = "ou=tty,dc=oms,dc=com"
LDAP_AUTH_CONNECTION_USERNAME = 'admin'
LDAP_AUTH_CONNECTION_PASSWORD = 'qwert@12345'