# -*- coding: utf-8 -*-
# author: itimor

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

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

# # Redis
# REDIS_OPTIONS = {
#     'HOST': '127.0.0.1',
#     'PORT': 6379,
#     'DB': 0
# }
# USE_REDIS = True
# # Channel settings
# CHANNEL_LAYERS = {
#     "default": {
#         # 'BACKEND': 'asgiref.inmemory.ChannelLayer',    #如果使用这个，消息变多时，会读不出来
#          "BACKEND": "asgi_redis.RedisChannelLayer",
#          "CONFIG": {
#              "hosts": ['redis://{}:{}'.format(REDIS_OPTIONS['HOST'],
#                                               REDIS_OPTIONS['PORT'])]
#          },
#         "ROUTING": "omsBackend.routing.channel_routing"
#     }
# }

# enail账号
MAIL_ACOUNT = {
    "mail_host": "mail.tb-gaming.com",
    "mail_user": "oms@tb-gaming.com",
    "mail_pass": "u62En68D9d",
    "mail_postfix": "tb-gaming.com",
}

#登录skype
from skpy import Skype
# skype账号
SK_ACOUNT = {
    'sk_user': 'oms@tb-gaming.com',
    'sk_pass': 'tengfa@918'
}
SK = Skype(SK_ACOUNT["sk_user"], SK_ACOUNT["sk_pass"])
#SK = 'skype'

TIME_ZONE = 'Asia/Shanghai'

import djcelery
djcelery.setup_loader()
# 这是使用了django-celery默认的数据库调度模型,任务执行周期都被存在你指定的orm数据库中
CELERYBEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler'

# celery settings
# celery中间人 redis://redis服务所在的ip地址:端口/数据库号
BROKER_URL = 'redis://192.168.6.110:6379/0'
# celery结果返回，可用于跟踪结果
CELERY_RESULT_BACKEND = 'redis://192.168.6.110:6379/0'

# celery内容等消息的格式设置
CELERY_ACCEPT_CONTENT = ['application/json', ]
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

# celery时区设置，使用settings中TIME_ZONE同样的时区
CELERY_TIMEZONE = TIME_ZONE