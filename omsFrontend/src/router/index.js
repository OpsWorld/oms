import Vue from 'vue'
import Router from 'vue-router'

const _import = require('./_import_' + process.env.NODE_ENV)
// in development-env not use lazy-loading, because lazy-loading too many pages will cause webpack hot update too slow. so only in production use lazy-loading;
// detail: https://panjiachen.github.io/vue-element-admin-site/#/lazy-loading

Vue.use(Router)

/* Layout */
import Layout from '../views/layout/Layout'

/**
 * hidden: true                   if `hidden:true` will not show in the sidebar(default is false)
 * redirect: noredirect           if `redirect:noredirect` will no redirct in the breadcrumb
 * name:'router-name'             the name is used by <keep-alive> (must set!!!)
 * meta : {
    role: ['admin','editor']     will control the page role (you can set multiple roles)
    title: 'title'               the name show in submenu and breadcrumb (recommend set)
    icon: 'svg-name'             the icon show in the sidebar,
    noCache: true                if fasle ,the page will no be cached(default is false)
  }
 **/
export const constantRouterMap = [
  { path: '/login', component: _import('login/index'), hidden: true },
  { path: '/404', component: _import('errorPage/404'), hidden: true },
  { path: '/403', component: _import('errorPage/403'), hidden: true },
  {
    path: '',
    component: Layout,
    icon: 'dashboard',
    redirect: 'dashboard',
    children: [{ path: 'dashboard', component: _import('dashboard/index'), name: '首页', icon: 'dashboard', meta: { noCache: true }
    }]
  },
  {
    name: '文档系统',
    path: '/wikis',
    component: Layout,
    icon: 'paper-plane',
    redirect: 'noredirect',
    children: [
      { path: 'wikiadmin', component: _import('wikis/wikiadmin'), name: '文档管理' },
      { path: 'addwiki', hidden: true, component: _import('wikis/components/addwiki'), name: '添加文档' },
      { path: 'editwiki/:wikiid', hidden: true, component: _import('wikis/components/editwiki'), name: '编辑文档' },
      { path: 'viewwiki/:wikiid', hidden: true, component: _import('wikis/components/viewwiki'), name: '查看文档' },
      { path: 'wikilist', component: _import('wikis/wikilist'), name: '文档中心' }
    ]
  }
]

export default new Router({
  // mode: 'history', //后端支持可开
  scrollBehavior: () => ({ y: 0 }),
  routes: constantRouterMap
})

export const asyncRouterMap = [
  {
    name: '工单系统',
    path: '/worktickets',
    component: Layout,
    icon: 'leaf',
    redirect: 'workticket',
    children: [
      { path: 'workticket', component: _import('worktickets/workticket'), name: '工单列表' },
      { path: 'tickettype', component: _import('worktickets/tickettype'), name: '工单类型' },
      { path: 'addworkticket', hidden: true, component: _import('worktickets/components/addworkticket'), name: '添加工单' },
      { path: 'editworkticket/:ticketid', hidden: true, component: _import('worktickets/components/editworkticket'), name: '编辑工单' }
    ]
  },
  {
    name: '第三支付对接',
    path: '/threepays',
    component: Layout,
    icon: 'bitcoin',
    redirect: 'threepay',
    children: [
      { path: 'paychannel', component: _import('threepays/paychannel'), name: '支付通道列表' },
      { path: 'platformpaychannels', component: _import('threepays/platformpaychannels'), name: '对接通道进度' },
      { path: 'merchant', component: _import('threepays/merchant'), name: '商户列表' },
      { path: 'paychannelname', component: _import('threepays/paychannelname'), name: '通道类型' }
    ]
  },
  {
    name: '研发管理',
    path: '/projects',
    component: Layout,
    icon: 'bug',
    redirect: 'projects',
    children: [
      { path: 'projects', component: _import('projects/projects'), name: '任务列表' },
      { path: 'projecttypes', component: _import('projects/projecttypes'), name: '任务类型' },
      { path: 'addproject', hidden: true, component: _import('projects/components/addproject'), name: '添加任务' },
      { path: 'editproject/:id', hidden: true, component: _import('projects/components/editproject'), name: '编辑任务' },
      { path: 'viewproject/:id', hidden: true, component: _import('projects/components/viewproject'), name: '查看任务' }
    ]
  },
  {
    name: '用户管理',
    path: '/users',
    component: Layout,
    icon: 'user',
    redirect: 'users',
    children: [
      { path: 'users', component: _import('users/users'), name: '用户列表' },
      { path: 'usergroups', component: _import('users/usergroups'), name: '用户组列表' },
      { path: 'roles', component: _import('users/roles'), name: '角色列表' }
    ]
  },
  {
    name: '菜单管理',
    path: '/menus',
    component: Layout,
    icon: 'fire',
    redirect: 'menus',
    children: [
      { path: 'menus', component: _import('menus/menus'), name: '菜单列表' },
      { path: 'menuperm', component: _import('menus/menuperm'), name: '菜单权限' }
    ]
  },
  {
    name: '主机管理',
    path: '/hosts',
    component: Layout,
    icon: 'desktop',
    redirect: 'hosts',
    children: [
      { path: 'hosts', component: _import('hosts/hosts'), name: '主机列表' },
      { path: 'assetrecords', component: _import('hosts/assetrecords'), name: '资产修改记录' },
      { path: 'idcs', component: _import('hosts/idcs'), name: '机房列表' }
    ]
  },
  {
    name: '发布系统',
    path: '/jobs',
    component: Layout,
    icon: 'tasks',
    redirect: 'jobs',
    children: [
      { path: 'jobs', component: _import('jobs/jobs'), name: '项目列表' },
      { path: 'addjob', hidden: true, component: _import('jobs/components/addjob'), name: '新建项目' },
      { path: 'editjob/:job_id', hidden: true, component: _import('jobs/components/editjob'), name: '编辑项目' },
      { path: 'runjob/:job_id', hidden: true, component: _import('jobs/components/runjob'), name: '构建项目' }
    ]
  },
  {
    name: '工具管理',
    path: '/tools',
    component: Layout,
    icon: 'cogs',
    redirect: 'upload',
    children: [
      { path: 'upload', component: _import('tools/upload'), name: '上传列表' },
      { path: 'opswikiadmin', component: _import('wikis/opswikiadmin'), name: '运维文档管理' },
      { path: 'addopswiki', hidden: true, component: _import('wikis/components/addopswiki'), name: '添加运维文档' },
      { path: 'editopswiki/:wikiid', hidden: true, component: _import('wikis/components/editopswiki'), name: '编辑运维文档' },
      { path: 'viewopswiki/:wikiid', hidden: true, component: _import('wikis/components/viewopswiki'), name: '查看运维文档' },
      { path: 'test', component: _import('tools/test'), name: '测试页面' }
    ]
  },
  {
    name: 'salt管理',
    path: '/salts',
    component: Layout,
    icon: 'cube',
    redirect: 'cmdrun',
    children: [
      { path: 'index', component: _import('salts/index'), name: 'salt状态' },
      { path: 'cmdrun', component: _import('salts/cmdrun'), name: '远程执行命令' }
    ]
  }
]

export const errorRouterMap = [
  { path: '*', redirect: '/404', hidden: true }
]
