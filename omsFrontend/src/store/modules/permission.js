import { asyncRouterMap, constantRouterMap } from '@/router'
import { getRouters } from '@/api/perm'

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
              accessedRouters = asyncRouterMap;
              commit('SET_ROUTERS', accessedRouters);
              localStorage.setItem('addRouters', JSON.stringify(accessedRouters));
        } else{
              getRouters().then(response => {
                  const myrouter = response.data[0];
                  const accessedRouters = generateRoutesFromMenu(asyncRouterMap, myrouter);
                  commit('SET_ROUTERS', accessedRouters);
                  localStorage.setItem('addRouters', JSON.stringify(accessedRouters));
              })
          }
        resolve()
      })
    }
  }
}

function generateRoutesFromMenu (asyncRouterMap, menus = [], routes = []) {
  for (var i of asyncRouterMap) {
    for (var j of menus) {
      var c = [];
      if (i.name == j.name) {
        if (i.children) {
            for (var m of i.children) {
              for (var n of j.children) {
                if (m.name == n.name) {
                  c.push(m)
                }
              }
            }
            i.children = c;
            routes.push(i);
        } else {
          routes.push(i);
        }
      }
    }
  }
  return routes
}

export default permission
