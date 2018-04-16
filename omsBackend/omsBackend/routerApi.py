# -*- coding: utf-8 -*-
# author: kiven

from rest_framework.routers import DefaultRouter

router = DefaultRouter()

from users.views import UserViewSet, RoleViewSet, GroupViewSet

router.register(r'users', UserViewSet)
router.register(r'groups', GroupViewSet)
router.register(r'roles', RoleViewSet)

from worktickets.views import WorkTicketViewSet, TicketCommentViewSet, TicketEnclosureViewSet, TicketTypeViewSet

router.register(r'worktickers', WorkTicketViewSet)
router.register(r'ticketcomments', TicketCommentViewSet)
router.register(r'ticketenclosures', TicketEnclosureViewSet)
router.register(r'tickettypes', TicketTypeViewSet)

from tools.views import UploadViewSet, SendmailViewSet, SendmessageViewSet, CalenderViewSet

router.register(r'upload', UploadViewSet)
router.register(r'sendmail', SendmailViewSet)
router.register(r'sendmessage', SendmessageViewSet)
router.register(r'calenders', CalenderViewSet)

from menus.views import FirstmenuViewSet, SecondmenuViewSet, ElementViewSet

router.register(r'firstmenus', FirstmenuViewSet)
router.register(r'secondmenus', SecondmenuViewSet)
router.register(r'menumetas', ElementViewSet)

from perms.views import UserMenuPermsViewSet, UserHostPermsViewSet, UserWikiPermsViewSet

router.register(r'usermenuperms', UserMenuPermsViewSet)
router.register(r'userhostperms', UserHostPermsViewSet)
router.register(r'userwikiperms', UserWikiPermsViewSet)

from threepay.views import (PlatformViewSet, MerchantViewSet, ThreePayEnclosureViewSet, PayChannelViewSet,
                            PayChannelNameViewSet, ThreePayCommentViewSet, PlatformPayChannelViewSet)

router.register(r'platforms', PlatformViewSet)
router.register(r'merchants', MerchantViewSet)
router.register(r'threepayenclosures', ThreePayEnclosureViewSet)
router.register(r'paychannels', PayChannelViewSet)
router.register(r'paychannelnames', PayChannelNameViewSet)
router.register(r'threepaycomments', ThreePayCommentViewSet)
router.register(r'platformpaychannels', PlatformPayChannelViewSet)

from wikis.views import WikiViewSet, OpsWikiViewSet

router.register(r'wikis', WikiViewSet)
router.register(r'opswikis', OpsWikiViewSet)

from hosts.views import HostViewSet, IdcViewSet, HostGroupViewSet

router.register(r'hosts', HostViewSet)
router.register(r'idcs', IdcViewSet)
router.register(r'hostgroups', HostGroupViewSet)

from jobs.views import JobsViewSet, DeployenvViewSet, DeploycmdViewSet, DeployJobsViewSet, DeployTicketViewSet, \
    DeployTicketEnclosureViewSet, SqlTicketTicketViewSet

router.register(r'jobs', JobsViewSet)
router.register(r'deployenvs', DeployenvViewSet)
router.register(r'deploycmds', DeploycmdViewSet)
router.register(r'deployjobs', DeployJobsViewSet)
router.register(r'deploytickets', DeployTicketViewSet)
router.register(r'deployticketenclosures', DeployTicketEnclosureViewSet)
router.register(r'sqltickets', SqlTicketTicketViewSet)

from records.views import RecordViewSet

router.register(r'records', RecordViewSet)

from projects.views import ProjectViewSet, ProjectCommentViewSet, ProjectEnclosureViewSet, ProjectTypeViewSet, \
    BugManagerViewSet, TestManagerViewSet, DemandManagerViewSet, DemandEnclosureViewSet

router.register(r'projects', ProjectViewSet)
router.register(r'projectcomments', ProjectCommentViewSet)
router.register(r'projectenclosures', ProjectEnclosureViewSet)
router.register(r'projecttypes', ProjectTypeViewSet)
router.register(r'bugmanagers', BugManagerViewSet)
router.register(r'testmanagers', TestManagerViewSet)
router.register(r'demandmanagers', DemandManagerViewSet)
router.register(r'demandenclosures', DemandEnclosureViewSet)

from optasks.views import OpsProjectViewSet, OpsDemandManagerViewSet

router.register(r'opsprojects', OpsProjectViewSet)
router.register(r'opsdemandmanagers', OpsDemandManagerViewSet)

from dnsmanager.views import DnsApiKeyViewSet, DnsDomainViewSet, DnsRecordViewSet, DnspodDomainViewSet, \
    DnspodRecordViewSet, GodaddyDomainViewSet, GodaddyRecordViewSet, BindDomainViewSet, BindRecordViewSet

router.register(r'dnsapikeys', DnsApiKeyViewSet)
router.register(r'dnsdomains', DnsDomainViewSet)
router.register(r'dnsrecords', DnsRecordViewSet)
router.register(r'dnspoddomains', DnspodDomainViewSet, base_name='dnspoddomains')
router.register(r'dnspodrecords', DnspodRecordViewSet, base_name='dnspodrecords')
router.register(r'godaddydomains', GodaddyDomainViewSet, base_name='godaddydomains')
router.register(r'godaddyreecords', GodaddyRecordViewSet, base_name='godaddyreecords')
router.register(r'binddomains', BindDomainViewSet, base_name='binddomains')
router.register(r'bindrecords', BindRecordViewSet, base_name='bindrecords')

from zkmanager.views import ZkUserViewSet, PunchViewSet, PunchSetViewSet

router.register(r'zkusers', ZkUserViewSet)
router.register(r'zkpunchs', PunchViewSet)
router.register(r'zkpunchset', PunchSetViewSet)
