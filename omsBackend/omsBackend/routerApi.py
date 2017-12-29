# -*- coding: utf-8 -*-
# author: kiven

from rest_framework.routers import DefaultRouter
from users.views import UserViewSet, RoleViewSet, GroupViewSet
from worktickets.views import WorkTicketViewSet, TicketCommentViewSet, TicketEnclosureViewSet, TicketTypeViewSet, TicketWikiViewSet
from threepay.views import PlatformViewSet, MerchantViewSet, ThreePayEnclosureViewSet, PayChannelViewSet, PayChannelNameViewSet,ThreePayCommentViewSet
from tools.views import UploadViewSet, SendmailViewSet, SendmessageViewSet
from menus.views import FirstmenuViewSet, SecondmenuViewSet, ElementViewSet
from perms.views import UserMenuPermsViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'groups', GroupViewSet)
router.register(r'roles', RoleViewSet)
router.register(r'worktickers', WorkTicketViewSet)
router.register(r'ticketcomments', TicketCommentViewSet)
router.register(r'ticketenclosures', TicketEnclosureViewSet)
router.register(r'tickettypes', TicketTypeViewSet)
router.register(r'ticketwikis', TicketWikiViewSet)
router.register(r'upload', UploadViewSet)
router.register(r'sendmail', SendmailViewSet)
router.register(r'sendmessage', SendmessageViewSet)
router.register(r'firstmenus', FirstmenuViewSet)
router.register(r'secondmenus', SecondmenuViewSet)
router.register(r'menumetas', ElementViewSet)
router.register(r'usermenuperms', UserMenuPermsViewSet)
router.register(r'platforms', PlatformViewSet)
router.register(r'merchants', MerchantViewSet)
router.register(r'threepayenclosures', ThreePayEnclosureViewSet)
router.register(r'paychannels', PayChannelViewSet)
router.register(r'paychannelnames', PayChannelNameViewSet)
router.register(r'threepaycomments', ThreePayCommentViewSet)
