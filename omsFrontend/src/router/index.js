import Vue from 'vue';
import VueRouter from 'vue-router';
import store from '../store'

Vue.use(VueRouter);

/* layout */
import Layout from '@/views/layout/Layout';

/**
 * icon : the icon show in the sidebar
 * hidden : if hidden:true will not show in the sidebar
 * redirect : if redirect:noredirect will not redirct in the levelbar
 * noDropdown : if noDropdown:true will not has submenu
 * meta : { role: ['admin'] }  will control the page role
 **/

export const constantRouterMap = [
    {path: '/login', component: require('@/views/login/login'), hidden: true},
    {path: '/404', component: require('@/views/error/404'), hidden: true},
    {path: '/401', component: require('@/views/error/401'), hidden: true},
    {
        name: 'dashboard',
        path: '/',
        component: require('@/views/layout/Layout'),
        redirect: '/dashboard',
        hidden: true,
        meta: {requiresAuth: true},
        children: [{path: 'dashboard', component: require('@/views/dashboard/index')}]
    }
];

export default  new VueRouter({
    // mode: 'history', //后端支持可开
    scrollBehavior: () => ({y: 0}),
    routes:constantRouterMap,
});


export const asyncRouterMap = [
    {
        name: '用户管理',
        path: '/users',
        component: require('@/views/layout/Layout'),
        icon: 'user',
        redirect: '/users/user',
        meta: {requiresAuth: true},
        children: [
            {path: 'user', component: require('@/views/users/user'), name: '用户列表'},
            {path: 'groups', component: require('@/views/users/usergroups'), name: '用户组列表'},
            {path: 'roles', component: require('@/views/users/roles'), name: '角色列表'},
        ]
    },
    {
        name: '工单管理',
        path: '/worktickets',
        component: require('@/views/layout/Layout'),
        icon: 'list',
        redirect: '/worktickets/workticket',
        meta: {requiresAuth: true},
        children: [
            {path: 'workticket', component: require('@/views/worktickets/workticket'), name: '工单列表'},
            {path: 'tickettype', component: require('@/views/worktickets/tickettype'), name: '工单类型'},
            {path: 'addworkticket', hidden: true, component: require('@/views/worktickets/addworkticket'), name: '添加工单'},
            {path: 'editworkticket/:id', hidden: true, component: require('@/views/worktickets/editworkticket'), name: '编辑工单'},
        ]
    },
    {
        name: '工具管理',
        path: '/tools',
        component: require('@/views/layout/Layout'),
        icon: 'cogs',
        redirect: '/tools/upload',
        meta: {requiresAuth: true},
        children: [
            {path: 'upload', component: require('@/views/tools/upload'), name: '上传管理'},
            {path: 'test', component: require('@/views/tools/test'), name: '测试页面'},
        ]
    },
    {name: '不存在', path: '*', redirect: '/404', hidden: true},
];
// 设置路由拦截
// 在vue-router的全局钩子中设置拦截
// 每个路由皆会的钩子函数
// to 进入 from 离开 next 传递
// router.beforeEach((to, from, next) => {
//     // console.log('to=', to.fullPath, '| from=', from.fullPath);
//     if (to.matched.some(record => record.meta.requiresAuth)) {
//         if (!store.state.user.islogin) {
//             _checkToken().then(res => {
//                 store.dispatch("GetUserInfo");
//                 next();
//             }, function () {
//                 next({
//                     path: '/login',
//                     query: {redirect: to.fullPath}
//                 })
//             });
//         } else {
//             _checkToken().then(function () {
//                 store.dispatch("GetUserInfo");
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
//
// export default router;