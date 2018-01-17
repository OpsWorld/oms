# -*- coding: utf-8 -*-
# author: kiven

from django.conf.urls import url
from salts import views

urlpatterns = [
    url(r'^get_all_key/', views.get_all_key),
    url(r'^minions_status/', views.minions_status),
    url(r'^get_minion_info/(?P<key_id>\w+)', views.get_minion_info),
    url(r'^cmdrun/', views.cmdrun),
    url(r'^get_result/(?P<jid>\w+)', views.get_result),
]
