# -*- coding: utf-8 -*-
# author: kiven

from rest_framework import viewsets
from wikis.models import Wiki
from wikis.serializers import WikiSerializer
from rest_framework.filters import SearchFilter

class WikiViewSet(viewsets.ModelViewSet):
    queryset = Wiki.objects.all().order_by('-update_time')
    serializer_class = WikiSerializer
    filter_backends = (SearchFilter,)
    search_fields = ['title', 'content', 'type__name']
    filter_fields = ['create_user__username']

