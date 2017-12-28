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
    'djcelery',  # 异步任务
    'worktickets',
    'tools',
    'users',
    'menus',
    'perms',
    'threepay',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, '../omsBackend.db'),
    }
}

# 使用ldap认证
# AUTHENTICATION_BACKENDS = ("django_python3_ldap.auth.LDAPBackend",)
LDAP_AUTH_URL = "ldap://192.168.6.101:389"
LDAP_AUTH_SEARCH_BASE = "ou=AllUser,dc=tb-gaming,dc=local"
LDAP_AUTH_CONNECTION_USERNAME = r'tb-gaming\itconfig'
LDAP_AUTH_CONNECTION_PASSWORD = r'TUjweiAHZQ'

# enail账号
MAIL_ACOUNT = {
    "mail_host": "mail.tb-gaming.com",
    "mail_user": "kiven@tb-gaming.com",
    "mail_pass": "ZfaEWFbcW5",
    "mail_postfix": "tb-gaming.com",
}

#登录skype
from skpy import Skype
# skype账号
SK_ACOUNT = {
    "sk_user": "tbkiven@outlook.com",
    "sk_pass": "tengfa9188"
}
#SK = Skype(SK_ACOUNT["sk_user"], SK_ACOUNT["sk_pass"])
SK = 'skype'