# -*- coding: utf-8 -*-
# author: itimor

from rest_framework import viewsets
from perms.models import UserMenuPerms
from perms.serializers import UserMenuPermsSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from menus.models import Firstmenu, Secondmenu, Element
from menus.serializers import FirstmenuSerializer, SecondmenuSerializer, ElementSerializer
from django.forms.models import model_to_dict
from users.models import User, Group
from users.serializers import UserSerializer, RoleSerializer, GroupSerializer
from perms.filters import UserMenuPermsFilter


class UserMenuPermsViewSet(viewsets.ModelViewSet):
    queryset = UserMenuPerms.objects.all()
    serializer_class = UserMenuPermsSerializer
    filter_class = UserMenuPermsFilter


@api_view()
def routers(request,username=None):
    userqueryset = User.objects.get(username=username)
    userserializer = UserSerializer(userqueryset, context={'request': request}).data
    groups = userserializer['groups']
    try:
        menus = []
        elements = []
        for group in groups:
            menuqueryset = UserMenuPerms.objects.get(group=group)
            menuserializer = UserMenuPermsSerializer(menuqueryset, context={'request': request}).data
            menus = menuserializer["firstmenus"] + menuserializer["secondmenus"] + menus
            elements = menuserializer["elements"] + elements
        menus = set(menus)
        elements = set(elements)
        return Response({"groups": groups, "menus": menus, "elements": elements})
    except Exception as e:
        raise e
        #return Response({"groups": groups, "menus": ['jjyy'], "elements": ['jjyy']})

# #根据不同用户生成不同的routers
# @api_view()
# def routers(request):
#     try:
#         queryset = UserMenuPerms.objects.get(user=request.user)
#         serializer = UserMenuPermsSerializer(queryset, context={'request': request}).data
#         routers = []
#         firstmenus = []
#         for onename in serializer['firstmenus']:
#             firstmenu = Firstmenu.objects.get(name=onename)
#             firstmenuserializer = FirstmenuSerializer(firstmenu, context={'request': request}).data
#             onenames = model_to_dict(firstmenu)
#             onenames["meta"] = {}
#             for meta_id in firstmenuserializer['meta']:
#                 menumeta = MenuMeta.objects.get(id=meta_id)
#                 menumetaserializer = MenuMetaSerializer(menumeta, context={'request': request}).data
#                 onenames["meta"][menumetaserializer["name"]] = menumetaserializer["action"]
#             onenames["children"] = []
#
#             for twoname in serializer['seaondmenus']:
#                 secondmenu = Secondmenu.objects.get(name=twoname)
#                 secondmenuserializer = SecondmenuSerializer(secondmenu, context={'request': request}).data
#                 twonames = model_to_dict(secondmenu)
#                 twonames["meta"] = {}
#                 for meta_id in secondmenuserializer['meta']:
#                     menumeta = MenuMeta.objects.get(id=meta_id)
#                     menumetaserializer = MenuMetaSerializer(menumeta, context={'request': request}).data
#                     twonames["meta"][menumetaserializer["name"]] = menumetaserializer["action"]
#                 if firstmenuserializer['name'] == secondmenuserializer['parent']:
#                     onenames["children"].append(twonames)
#
#             firstmenus.append(onenames)
#         routers.append(firstmenus)
#         return Response(routers)
#     except Exception as e:
#         return Response(status=status.HTTP_404_NOT_FOUND)
