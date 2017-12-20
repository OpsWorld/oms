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
  { path: '/authredirect', component: _import('login/authredirect'), hidden: true },
  { path: '/404', component: _import('errorPage/404'), hidden: true },
  { path: '/401', component: _import('errorPage/401'), hidden: true },
  {
    path: '',
    component: Layout,
    redirect: 'dashboard',
    children: [{
      path: 'dashboard',
      component: _import('dashboard/index'),
      name: 'dashboard',
      icon: 'dashboard',
      meta: { noCache: true }
    }]
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
      { path: 'editworkticket/:ticketid', hidden: true, component: _import('worktickets/components/editworkticket'), name: 'editworkticket', authority: '编辑工单' },
      { path: 'platform', component: _import('worktickets/platform'), name: 'platform', authority: '第三支付平台' },
      { path: 'merchant', component: _import('worktickets/merchant'), name: 'merchant', authority: '第三支付商户' }
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
  },
  {
    name: 'deployManager',
    path: '/deploys',
    component: Layout,
    icon: 'flag',
    redirect: 'noredirect',
    authority: '发布管理',
    children: [
    ]
  }
]

export const errorRouterMap = [
  { path: '*', redirect: '/404', hidden: true }
]
