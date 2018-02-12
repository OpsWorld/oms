# -*- coding: utf-8 -*-
# author: kiven

from rest_framework import viewsets
from wikis.models import Wiki, OpsWiki
from wikis.serializers import WikiSerializer, OpsWikiSerializer
from wikis.filters import WikiFilterBackend
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter


class WikiViewSet(viewsets.ModelViewSet):
    queryset = Wiki.objects.all().order_by('-update_time')
    serializer_class = WikiSerializer
    filter_backends = (WikiFilterBackend, DjangoFilterBackend, SearchFilter)
    search_fields = ['title', 'content']
    filter_fields = ['create_user__username', 'type__name']


class OpsWikiViewSet(viewsets.ModelViewSet):
    queryset = OpsWiki.objects.all().order_by('-update_time')
    serializer_class = OpsWikiSerializer
    search_fields = ['title', 'content']