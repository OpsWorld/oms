import { asyncRouterMap, constantRouterMap } from '@/router'

const permission = {
  state: {
    routers: constantRouterMap,
    addRouters: JSON.parse(localStorage.getItem('addRouters')),
  },
  mutations: {
    SET_ROUTERS: (state, routers) => {
      state.addRouters = routers,
      state.routers = constantRouterMap.concat(routers)
    }
  },
  actions: {
    GenerateRoutes({ commit }, data) {
      return new Promise(resolve => {
        const { username } = data
        let accessedRouters
        if (username.indexOf('admin') >= 0) {
          accessedRouters = asyncRouterMap
        } else {
          accessedRouters = filterAsyncRouter(asyncRouterMap, username)
        }
          commit('SET_ROUTERS', []);
          commit('SET_ROUTERS', accessedRouters);
          localStorage.setItem('addRouters', JSON.stringify([]));
          localStorage.setItem('addRouters', JSON.stringify(accessedRouters));
        resolve()
      })
    }
  }
}

/**
 * 通过meta.role判断是否与当前用户权限匹配
 * @param username
 * @param route
 */
function hasPermission(username, route) {
  if (route.meta && route.meta.role) {
    return username.some(role => route.meta.role.indexOf(role) >= 0)
  } else {
    return true
  }
}

/**
 * 递归过滤异步路由表，返回符合用户角色权限的路由表
 * @param asyncRouterMap
 * @param username
 */
function filterAsyncRouter(asyncRouterMap, username) {
  const accessedRouters = asyncRouterMap.filter(route => {
    if (hasPermission(username, route)) {
      if (route.children && route.children.length) {
        route.children = filterAsyncRouter(route.children, username)
      }
      return true
    }
    return false
  })
  return accessedRouters
}

export default permission
