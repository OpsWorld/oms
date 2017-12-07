import router from './router'
import store from './store'
import NProgress from 'nprogress' // Progress 进度条
import 'nprogress/nprogress.css'// Progress 进度条样式
import { Message } from 'element-ui'

// permissiom judge
function hasPermission(roles, permissionRoles) {
  if (roles.indexOf('admin') >= 0) return true // admin权限 直接通过
  if (!permissionRoles) return true
  return roles.some(role => permissionRoles.indexOf(role) >= 0)
}

const whiteList = ['/login', '/authredirect']// 不重定向白名单

router.beforeEach((to, from, next) => {
  NProgress.start() // 开启Progress
  if (store.getters.islogin) { // 判断是否有token
    if (to.path === '/login') {
      next({ path: '/' })
      NProgress.done() // router在hash模式下 手动改变hash 重定向回来 不会触发afterEach 暂时hack方案 ps：history模式下无问题，可删除该行！
    } else {
        _checkToken().then(res => {
            const username = localStorage.getItem('username');
            store.dispatch('GenerateRoutes', { username }).then(() => { // 生成可访问的路由表
                router.addRoutes(store.getters.addRouters); // 动态添加可访问路由表
                next({ ...to }) // hack方法 确保addRoutes已完成
            })
                next();
            }, function () {
                next({
                    path: '/login',
                    query: {redirect: to.fullPath}
                })
            })
    }
  } else {
    if (whiteList.indexOf(to.path) !== -1) { // 在免登录白名单，直接进入
      next()
    } else {
      next('/login') // 否则全部重定向到登录页
      NProgress.done() // router在hash模式下 手动改变hash 重定向回来 不会触发afterEach 暂时hack方案 ps：history模式下无问题，可删除该行！
    }
  }
})

/**
 * Token验证，Token验证是否有效，时间验证过期
 * */
function _checkToken() {
    return new Promise(function (resolve, reject) {
        const token = localStorage.getItem('token');
        const token_time = localStorage.getItem('token_time');
        const now_time = new Date().getTime();  // 毫秒数，token过期时间为 2小时
        if (token && (now_time - token_time) < 1000 * 60 * 60 * 2) {
            // 设置全局请求的token， 参考 https://segmentfault.com/q/1010000008595567/a-1020000008596744
            resolve();
        } else {
            localStorage.removeItem('token');
            localStorage.removeItem('token_time');
            reject();
        }
    })
}

router.afterEach(() => {
  NProgress.done() // 结束Progress
})
