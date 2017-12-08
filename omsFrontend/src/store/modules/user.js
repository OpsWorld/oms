import { login, logout, getUserInfo } from '@/api/login'
import { getRouterInfo } from '@/api/perm'

const user = {
  state: {
    token: sessionStorage.getItem('token'),
    username: sessionStorage.getItem('username'),
    groups: [],
    menus: undefined,
    eleemnts: undefined,
    permissionMenus: undefined
  },

  mutations: {
    SET_TOKEN: (state, token) => {
      state.token = token
    },
    SET_USERNAME: (state, username) => {
      state.username = username
    },
    SET_GROUPS: (state, groups) => {
      state.groups = groups
    },
    SET_MENUS: (state, menus) => {
      state.menus = menus
    },
    SET_ELEMENTS: (state, elements) => {
      state.elements = elements
    },
    SET_PERMISSION_MENUS: (state, permissionMenus) => {
      state.permissionMenus = permissionMenus
    }
  },

  actions: {
    // 用户名登录
    Login({ commit }, userInfo) {
      return new Promise((resolve, reject) => {
        login(userInfo).then(response => {
          commit('SET_TOKEN', response.data.token)
          commit('SET_USERNAME', userInfo.username)
          sessionStorage.setItem('username', userInfo.username)
          sessionStorage.setItem('token', response.data.token)
          commit('SET_MENUS', undefined)
          commit('SET_ELEMENTS', undefined)
          resolve()
        }).catch(error => {
          reject(error)
        })
      })
    },

    // 获取用户信息
    GetUserInfo({ commit }) {
      return new Promise((resolve, reject) => {
        getRouterInfo().then(response => {
          const data = response.data
          const groups = data.groups
          commit('SET_GROUPS', groups)
          const menus = {}
          for (const i of data.menus) {
            menus[i] = true
          }
          commit('SET_MENUS', menus)
          const elements = {}
          for (const i of data.elements) {
            elements[i] = true
          }
          commit('SET_ELEMENTS', elements)
          // sessionStorage.setItem('groups', groups)
          // const menus = {}
          // const elements = {}
          // for (let i = 0; i < groups.length; i++) {
          //   const params = { group: groups[i] }
          //   getMenuPerm(params).then(response => {
          //     const data = response.data.results[0]
          //     for (let i = 0; i < data.firstmenus.length; i++) {
          //       menus[data.firstmenus[i]] = true
          //     }
          //     for (let i = 0; i < data.secondmenus.length; i++) {
          //       menus[data.secondmenus[i]] = true
          //     }
          //     for (let i = 0; i < data.elements.length; i++) {
          //       elements[data.elements[i]] = true
          //     }
          //   })
          // }
          // commit('SET_MENUS', menus)
          // commit('SET_ELEMENTS', elements)
          resolve(response)
        }).catch(error => {
          reject(error)
        })
      })
    },

    // 登出
    LogOut({ commit, state }) {
      return new Promise((resolve, reject) => {
        logout(state.token).then(() => {
          commit('SET_TOKEN', '')
          commit('SET_GROUPS', [])
          sessionStorage.removeItem('token')
          sessionStorage.removeItem('groups')
          commit('SET_MENUS', undefined)
          commit('SET_ELEMENTS', undefined)
          commit('SET_PERMISSION_MENUS', undefined)
          resolve()
        }).catch(error => {
          reject(error)
        })
      })
    },

    // 前端 登出
    FedLogOut({ commit }) {
      return new Promise(resolve => {
        commit('SET_TOKEN', '')
        sessionStorage.removeItem('token')
        commit('SET_MENUS', undefined)
        commit('SET_ELEMENTS', undefined)
        commit('SET_PERMISSION_MENUS', undefined)
        resolve()
      })
    },

    // 动态修改权限
    ChangeRole({ commit, state }, groups) {
      return new Promise(resolve => {
        commit('SET_TOKEN', groups)
        sessionStorage.setItem('groups', groups)
        getUserInfo(state.username).then(response => {
          const data = response.data.results[0]
          commit('SET_GROUPS', data.groups)
          sessionStorage.setItem('groups', data.groups)
          resolve()
        })
      })
    }
  }
}

export default user
