# -*- coding: utf-8 -*-
# author: kiven

from rest_framework.routers import DefaultRouter
from users.views import UserViewSet, GroupViewSet, RoleViewSet
from worktickets.views import WorkTicketViewSet, TicketCommentViewSet, TicketEnclosureViewSet, TicketTypeViewSet, \
    TicketWikiViewSet
from tools.views import UploadViewSet
from menus.views import FirstmenuViewSet, SecondmenuViewSet, MenuMetaViewSet
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
router.register(r'firstmenus', FirstmenuViewSet)
router.register(r'secondmenus', SecondmenuViewSet)
router.register(r'menumetas', MenuMetaViewSet)
router.register(r'usermenuperms', UserMenuPermsViewSet)
