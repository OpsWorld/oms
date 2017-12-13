# -*- coding: utf-8 -*-
# author: kiven

from rest_framework.routers import DefaultRouter
from users.views import UserViewSet, RoleViewSet, GroupViewSet
from worktickets.views import WorkTicketViewSet, TicketCommentViewSet, TicketEnclosureViewSet, TicketTypeViewSet, \
    TicketWikiViewSet
from tools.views import UploadViewSet, SendmailViewSet
from menus.views import FirstmenuViewSet, SecondmenuViewSet, ElementViewSet
from perms.views import UserMenuPermsViewSet
from cmd.views import CmdrunViewSet

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
router.register(r'firstmenus', FirstmenuViewSet)
router.register(r'secondmenus', SecondmenuViewSet)
router.register(r'menumetas', ElementViewSet)
router.register(r'usermenuperms', UserMenuPermsViewSet)
router.register(r'cmdrun', CmdrunViewSet)
