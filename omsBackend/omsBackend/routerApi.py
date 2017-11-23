# -*- coding: utf-8 -*-
# author: kiven

from rest_framework.routers import DefaultRouter
from users.views import UserViewSet, GroupViewSet, RoleViewSet
from tickets.views import WorkTicketViewSet, TicketCommentViewSet, TicketEnclosureViewSet, TicketTypeViewSet, TicketWikiViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'groups', GroupViewSet)
router.register(r'roles', RoleViewSet)
router.register(r'worktickers', WorkTicketViewSet)
router.register(r'ticketcomments', TicketCommentViewSet)
router.register(r'ticketenclosures', TicketEnclosureViewSet)
router.register(r'tickettypes', TicketTypeViewSet)
router.register(r'ticketwikis', TicketWikiViewSet)

