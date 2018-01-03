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
    children: [{ path: 'dashboard', component: _import('dashboard/index'), name: 'dashboard', icon: 'dashboard', meta: { noCache: true }
    }]
  },
  {
    name: 'wikiManager',
    path: '/wikis',
    component: Layout,
    icon: 'flag',
    redirect: 'noredirect',
    authority: '文档系统',
    children: [
      { path: 'wikiadmin', component: _import('wikis/wikiadmin'), name: 'wikiadmin', authority: '文档管理' },
      { path: 'addwiki', hidden: true, component: _import('wikis/components/addwiki'), name: 'addwiki', authority: '添加文档' },
      { path: 'editwiki/:wikiid', hidden: true, component: _import('wikis/components/editwiki'), name: 'editwiki', authority: '编辑文档' },
      { path: 'viewwiki/:wikiid', hidden: true, component: _import('wikis/components/viewwiki'), name: 'viewwiki', authority: '查看文档' },
      { path: 'wikilist', component: _import('wikis/wikilist'), name: 'wikilist', authority: '文档中心' }
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
    name: 'userManager',
    path: '/users',
    component: Layout,
    icon: 'user',
    redirect: 'users',
    authority: '用户管理',
    children: [
      { path: 'users', component: _import('users/users'), name: 'userlist', authority: '用户列表' },
      { path: 'usergroups', component: _import('users/usergroups'), name: 'grouplist', authority: '用户组列表' },
      { path: 'roles', component: _import('users/roles'), name: 'rolelist', authority: '角色列表' }
    ]
  },
  {
    name: 'ticketManager',
    path: '/worktickets',
    component: Layout,
    icon: 'leaf',
    redirect: 'workticket',
    authority: '工单系统',
    children: [
      { path: 'workticket', component: _import('worktickets/workticket'), name: 'workticketlist', authority: '工单列表' },
      { path: 'tickettype', component: _import('worktickets/tickettype'), name: 'tickettypelist', authority: '工单类型' },
      { path: 'addworkticket', hidden: true, component: _import('worktickets/components/addworkticket'), name: 'addworkticket', authority: '添加工单' },
      { path: 'editworkticket/:ticketid', hidden: true, component: _import('worktickets/components/editworkticket'), name: 'editworkticket', authority: '编辑工单' }
    ]
  },
  {
    name: 'threepayManager',
    path: '/threepays',
    component: Layout,
    icon: 'strikethrough',
    redirect: 'threepay',
    authority: '第三支付对接',
    children: [
      { path: 'paychannel', component: _import('threepays/paychannel'), name: 'paychannel', authority: '支付通道列表' },
      { path: 'paychannelname', component: _import('threepays/paychannelname'), name: 'paychannelname', authority: '通道类型' }
    ]
  },
  {
    name: 'toolManager',
    path: '/tools',
    component: Layout,
    icon: 'cogs',
    redirect: 'upload',
    authority: '工具管理',
    children: [
      { path: 'upload', component: _import('tools/upload'), name: 'upload', authority: '上传列表' },
      { path: 'sendmessage', component: _import('tools/sendmessage'), name: 'sendmessage', authority: '消息列表' },
      { path: 'test', component: _import('tools/test'), name: 'test', authority: '测试页面' }
    ]
  },
  {
    name: 'menuManager',
    path: '/menus',
    component: Layout,
    icon: 'fire',
    redirect: 'menus',
    authority: '菜单管理',
    children: [
      { path: 'menus', component: _import('menus/menus'), name: 'menulist', authority: '菜单列表' },
      { path: 'menuperm', component: _import('menus/menuperm'), name: 'menuperm', authority: '菜单权限' }
    ]
  }
]

export const errorRouterMap = [
  { path: '*', redirect: '/404', hidden: true }
]
