import Vue from 'vue';
import VueRouter from 'vue-router';
import store from '../../store'

Vue.use(VueRouter);

/* layout */
import Layout from '@/views/layout/Layout';

/* dashboard */
import Dashboard from '@/views/dashboard/index';

/* user */
import Userlist from '@/views/users/user'
import Grouplist from '@/views/users/usergroups'
import Rolelist from '@/views/users/roles'

/* workticket */
import Workticket from '@/views/worktickets/workticket'
import Tickettype from '@/views/worktickets/tickettype'
import addWorkticket from '@/views/worktickets/addworkticket'
import editWorkticket from '@/views/worktickets/editworkticket'

/* tools */
import Upload from '@/views/tools/upload'
import Test from '@/views/tools/test'

/**
 * icon : the icon show in the sidebar
 * hidden : if hidden:true will not show in the sidebar
 * redirect : if redirect:noredirect will not redirct in the levelbar
 * noDropdown : if noDropdown:true will not has submenu
 * meta : { role: ['admin'] }  will control the page role
 **/

export const routes = [
    {path: '/login', component: require('@/views/login/login'), hidden: true},
    {path: '/404', component: require('@/views/error/404'), hidden: true},
    {path: '/401', component: require('@/views/error/401'), hidden: true},
    {path: '*', redirect: '/404', hidden: true},
    {
        path: '/',
        component: Layout,
        redirect: '/dashboard',
        name: 'dashboard',
        hidden: true,
        meta: {requiresAuth: true},
        children: [{path: 'dashboard', component: Dashboard}]
    },
    {
        path: '/users',
        component: Layout,
        redirect: '/users/user',
        name: '用户管理',
        icon: 'user',
        meta: {requiresAuth: true},
        children: [
            {path: 'user', component: Userlist, name: '用户列表'},
            {path: 'groups', component: Grouplist, name: '用户组列表'},
            {path: 'roles', component: Rolelist, name: '角色列表'},
        ]
    },
    {
        path: '/worktickets',
        component: Layout,
        redirect: '/worktickets/workticket',
        name: '工单管理',
        icon: 'list',
        meta: {requiresAuth: true},
        children: [
            {path: 'workticket', component: Workticket, name: '工单列表'},
            {path: 'tickettype', component: Tickettype, name: '工单类型'},
            {path: 'addworkticket', hidden: true, component: addWorkticket, name: '添加工单'},
            {path: 'editworkticket/:id', hidden: true, component: editWorkticket, name: '编辑工单'},
        ]
    },
    {
        path: '/tools',
        component: Layout,
        redirect: '/tools/upload',
        name: '工具管理',
        icon: 'cogs',
        meta: {requiresAuth: true},
        children: [
            {path: 'upload', component: Upload, name: '上传管理'},
            {path: 'test', component: Test, name: '测试页面'},
        ]
    },
];

export default new VueRouter({
    // mode: 'history', //后端支持可开
    scrollBehavior: () => ({y: 0}),
    routes
});

// // 设置路由拦截
// // 在vue-router的全局钩子中设置拦截
// // 每个路由皆会的钩子函数
// // to 进入 from 离开 next 传递
// router.beforeEach((to, from, next) => {
//     // console.log('to=', to.fullPath, '| from=', from.fullPath);
//     if (to.matched.some(record => record.meta.requiresAuth)) {
//         if (!store.state.user.islogin) {
//             _checkToken().then(res => {
//                 store.dispatch("getUserInfo");
//                 next();
//             }, function () {
//                 next({
//                     path: '/login',
//                     query: {redirect: to.fullPath}
//                 })
//             });
//         } else {
//             _checkToken().then(function () {
//                 store.dispatch("getUserInfo");
//                 next();
//             }, function () {
//                 next({
//                     path: '/login'
//                 })
//             });
//         }
//     } else {
//         next(); // 确保一定要调用 next()
//     }
// })
//
// /**
//  * Token验证，Token验证是否有效，时间验证过期
//  * */
// function _checkToken() {
//     return new Promise(function (resolve, reject) {
//         const token = localStorage.getItem('token');
//         const token_time = localStorage.getItem('token_time');
//         const now_time = new Date().getTime();  // 毫秒数，token过期时间为 2小时
//         if (token && (now_time - token_time) < 1000 * 60 * 60 * 2) {
//             // 设置全局请求的token， 参考 https://segmentfault.com/q/1010000008595567/a-1020000008596744
//             resolve();
//         } else {
//             localStorage.removeItem('token');
//             localStorage.removeItem('token_time');
//             reject();
//         }
//     })
// }

// Menu should have 2 levels.
function generateRoutesFromMenu (menu = [], routes = []) {
  for (let i = 0, l = menu.length; i < l; i++) {
    let item = menu[i];
    if (item.path) {
      routes.push(item)
    }
    if (!item.component) {
      // item.component = resolve => require([`views/${item.component}.vue`], resolve)
      generateRoutesFromMenu(item.children, routes)
    }
  }
  return routes
}