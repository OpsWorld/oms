# -*- coding: utf-8 -*-
# author: itimor

import os

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

#登录skype
from skpy import Skype
# skype账号
SK_ACOUNT = {
    "sk_user": "tbkiven@outlook.com",
    "sk_pass": "tengfa9188"
}
#SK = Skype(SK_ACOUNT["sk_user"], SK_ACOUNT["sk_pass"])
SK = 'skype'

TIME_ZONE = 'Asia/Shanghai'

import djcelery
djcelery.setup_loader()
# 这是使用了django-celery默认的数据库调度模型,任务执行周期都被存在你指定的orm数据库中
CELERYBEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler'

# celery内容等消息的格式设置
CELERY_ACCEPT_CONTENT = ['application/json', ]
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

# celery时区设置，使用settings中TIME_ZONE同样的时区
CELERY_TIMEZONE = TIME_ZONE