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

# Redis
REDIS_OPTIONS = {
    'HOST': '127.0.0.1',
    'PORT': 6379,
    'DB': 0
}
USE_REDIS = True
# Channel settings
CHANNEL_LAYERS = {
    "default": {
        # 'BACKEND': 'asgiref.inmemory.ChannelLayer',    #如果使用这个，消息变多时，会读不出来
         "BACKEND": "asgi_redis.RedisChannelLayer",
         "CONFIG": {
             "hosts": ['redis://{}:{}'.format(REDIS_OPTIONS['HOST'],
                                              REDIS_OPTIONS['PORT'])]
         },
        "ROUTING": "omsBackend.routing.channel_routing"
    }
}