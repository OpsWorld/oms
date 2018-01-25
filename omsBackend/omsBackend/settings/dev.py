# -*- coding: utf-8 -*-
# author: itimor

import os

TIME_ZONE = 'Asia/Shanghai'

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

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

# 登录skype
from skpy import Skype

# skype账号
SK_ACOUNT = {
    "sk_user": "tbkiven@outlook.com",
    "sk_pass": "tengfa9188"
}
# SK = Skype(SK_ACOUNT["sk_user"], SK_ACOUNT["sk_pass"])
SK = 'skype'

REDIS_URL = 'redis://127.0.0.1:6379/'
# celery配置
CELERY_BROKER_URL = REDIS_URL + '0'

# celery结果返回，可用于跟踪结果
CELERY_RESULT_BACKEND = 'django-db'

# celery内容等消息的格式设置
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'

# celery时区设置，使用settings中TIME_ZONE同样的时区
CELERY_TIMEZONE = TIME_ZONE

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": REDIS_URL + '1',
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

# saltapi
# salt_info = {
#     "url": "http://192.168.6.99:8080",
#     "username": "salt",
#     "password": "123"
# }
salt_info = {
    "url": "http://salt.tbsysmanager.com:8080",
    "username": "saltdev",
    "password": "FF01VeF4hs1FqZ5M"
}

from salts.saltapi import SaltAPI
sapi = SaltAPI(url=salt_info["url"], username=salt_info["username"], password=salt_info["password"])
