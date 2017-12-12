import { asyncRouterMap, constantRouterMap, errorRouterMap } from '@/router'

/**
 * 通过authority判断是否与当前用户权限匹配
 * @param menus
 * @param route
 */
function hasPermission(menus, route) {
  if (route.authority) {
    if (menus[route.authority] !== undefined) {
      console.log(route.authority)
      return menus[route.authority]
    } else {
      return false
    }
  } else {
    return true
  }
}

/**
 * 递归过滤异步路由表，返回符合用户角色权限的路由表
 * @param asyncRouterMap
 * @param groups
 */
function filterAsyncRouter(asyncRouterMap, menus) {
  const accessedRouters = asyncRouterMap.filter(route => {
    if (hasPermission(menus, route)) {
      if (route.children && route.children.length) {
        route.children = filterAsyncRouter(route.children, menus)
      }
      return true
    }
    return false
  })
  return accessedRouters
}

const permission = {
  state: {
    routers: constantRouterMap,
    addRouters: []
  },
  mutations: {
    SET_ROUTERS: (state, routers) => {
      state.addRouters = routers
      state.routers = constantRouterMap.concat(routers)
    }
  },
  actions: {
    GenerateRoutes({ commit }, { role, menus }) {
      return new Promise(resolve => {
        let accessedRouters
        if (role === 'super') {
          commit('SET_ROUTERS', accessedRouters)
          accessedRouters = asyncRouterMap.concat(errorRouterMap)
        } else {
          accessedRouters = filterAsyncRouter(asyncRouterMap, menus).concat(errorRouterMap)
        }
        commit('SET_ROUTERS', accessedRouters)
        resolve()
      })
    }
  }
}

export default permission
