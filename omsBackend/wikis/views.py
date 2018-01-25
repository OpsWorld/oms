# -*- coding: utf-8 -*-
# author: kiven

from rest_framework import viewsets
from wikis.models import Wiki, OpsWiki
from wikis.serializers import WikiSerializer, OpsWikiSerializer


class WikiViewSet(viewsets.ModelViewSet):
    queryset = Wiki.objects.all().order_by('-update_time')
    serializer_class = WikiSerializer
    search_fields = ['title', 'content']
    filter_fields = ['create_user__username', 'type__name']


class OpsWikiViewSet(viewsets.ModelViewSet):
    queryset = OpsWiki.objects.all().order_by('-update_time')
    serializer_class = OpsWikiSerializer
    search_fields = ['title', 'content']