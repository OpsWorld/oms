import router from './router'
import store from './store'
import NProgress from 'nprogress' // Progress 进度条
import 'nprogress/nprogress.css'// Progress 进度条样式
import { Message } from 'element-ui'

// permissiom judge
function hasPermission(groups, permissionGroups) {
  if (groups.indexOf('admin') >= 0) return true // admin权限 直接通过
  if (!permissionGroups) return true
  return groups.some(group => permissionGroups.indexOf(group) >= 0)
}

const whiteList = ['/login']// 不重定向白名单

router.beforeEach((to, from, next) => {
  NProgress.start() // 开启Progress
  if (localStorage.getItem('token')) { // 判断是否有token
    if (to.path === '/login') {
      next({ path: '/' })
      NProgress.done() // router在hash模式下 手动改变hash 重定向回来 不会触发afterEach 暂时hack方案 ps：history模式下无问题，可删除该行！
    } else {
      if (store.getters.role.length === 0) { // 判断当前用户是否已拉取完user_info信息
        store.dispatch('GetUserInfo').then(response => { // 拉取user_info
          const role = store.getters.role
          const menus = store.getters.menus
          store.dispatch('GenerateRoutes', { role, menus }).then(() => { // 生成可访问的路由表
            router.addRoutes(store.getters.addRouters) // 动态添加可访问路由表
            next({ ...to, replace: true }) // hack方法 确保addRoutes已完成 ,replace: true so the navigation will not leave a history record
          })
        }).catch(() => {
          store.dispatch('FedLogOut').then(() => {
            Message.error('验证失败,请重新登录')
            console.log('not found groups')
            next({ path: '/login' })
          })
        })
      } else {
        // 没有动态改变权限的需求可直接next() 删除下方权限判断 ↓
        if (hasPermission(store.getters.groups, to.meta.group)) {
          next()//
        } else {
          next({ path: '/403', query: { noGoBack: true }})
          NProgress.done() // router在hash模式下 手动改变hash 重定向回来 不会触发afterEach 暂时hack方案 ps：history模式下无问题，可删除该行！
        }
      }
    }
  } else {
    console.log("haven't token")
    if (whiteList.indexOf(to.path) !== -1) { // 在免登录白名单，直接进入
      next()
    } else {
      next({
        path: '/login',
        query: { redirect: to.fullPath }
      }) // 否则全部重定向到登录页
      NProgress.done() // router在hash模式下 手动改变hash 重定向回来 不会触发afterEach 暂时hack方案 ps：history模式下无问题，可删除该行！
    }
  }
})

router.afterEach(() => {
  NProgress.done() // 结束Progress
})

/**
 * Token验证，Token验证是否有效，时间验证过期
 * */
// function _checkToken() {
//   return new Promise(function(resolve, reject) {
//     const token = localStorage.getItem('token')
//     const token_time = localStorage.getItem('token_time')
//     const now_time = new Date().getTime()
//     // 毫秒数，token过期时间为 2小时
//     if (token && (now_time - token_time) < 1000 * 60 * 60 * 2) {
//       // 设置全局请求的token， 参考 https://segmentfault.com/q/1010000008595567/a-1020000008596744
//       resolve()
//     } else {
//       localStorage.removeItem('token')
//       localStorage.removeItem('token_time')
//       reject()
//     }
//   })
// }
