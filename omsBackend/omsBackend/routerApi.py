# -*- coding: utf-8 -*-
# author: kiven

from rest_framework.routers import DefaultRouter
from users.views import UserViewSet, RoleViewSet, GroupViewSet
from worktickets.views import WorkTicketViewSet, TicketCommentViewSet, TicketEnclosureViewSet, TicketTypeViewSet
from threepay.views import (PlatformViewSet, MerchantViewSet, ThreePayEnclosureViewSet, PayChannelViewSet,
                            PayChannelNameViewSet, ThreePayCommentViewSet, PlatformPayChannelViewSet)
from tools.views import UploadViewSet, SendmailViewSet, SendmessageViewSet, CalenderViewSet
from menus.views import FirstmenuViewSet, SecondmenuViewSet, ElementViewSet
from perms.views import UserMenuPermsViewSet, UserHostPermsViewSet, UserWikiPermsViewSet
from wikis.views import WikiViewSet, OpsWikiViewSet
from hosts.views import HostViewSet, IdcViewSet, HostGroupViewSet
from jobs.views import JobsViewSet, DeployJobsViewSet, DeploycmdViewSet
from records.views import RecordViewSet
from projects.views import ProjectViewSet, ProjectCommentViewSet, ProjectTypeViewSet

router = DefaultRouter()

router.register(r'users', UserViewSet)
router.register(r'groups', GroupViewSet)
router.register(r'roles', RoleViewSet)

router.register(r'worktickers', WorkTicketViewSet)
router.register(r'ticketcomments', TicketCommentViewSet)
router.register(r'ticketenclosures', TicketEnclosureViewSet)
router.register(r'tickettypes', TicketTypeViewSet)

router.register(r'upload', UploadViewSet)
router.register(r'sendmail', SendmailViewSet)
router.register(r'sendmessage', SendmessageViewSet)
router.register(r'calenders', CalenderViewSet)

router.register(r'firstmenus', FirstmenuViewSet)
router.register(r'secondmenus', SecondmenuViewSet)
router.register(r'menumetas', ElementViewSet)

router.register(r'usermenuperms', UserMenuPermsViewSet)
router.register(r'userhostperms', UserHostPermsViewSet)
router.register(r'userwikiperms', UserWikiPermsViewSet)

router.register(r'platforms', PlatformViewSet)
router.register(r'merchants', MerchantViewSet)
router.register(r'threepayenclosures', ThreePayEnclosureViewSet)
router.register(r'paychannels', PayChannelViewSet)
router.register(r'paychannelnames', PayChannelNameViewSet)
router.register(r'threepaycomments', ThreePayCommentViewSet)
router.register(r'platformpaychannels', PlatformPayChannelViewSet)

router.register(r'wikis', WikiViewSet)
router.register(r'opswikis', OpsWikiViewSet)

router.register(r'hosts', HostViewSet)
router.register(r'idcs', IdcViewSet)
router.register(r'hostgroups', HostGroupViewSet)

router.register(r'jobs', JobsViewSet)
router.register(r'deployjobs', DeployJobsViewSet)
router.register(r'deploycmds', DeploycmdViewSet)

router.register(r'records', RecordViewSet)

router.register(r'projects', ProjectViewSet)
router.register(r'projectcomments', ProjectCommentViewSet)
router.register(r'projecttypes', ProjectTypeViewSet)
