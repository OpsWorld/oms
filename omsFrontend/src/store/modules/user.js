import { login, logout, getUserInfo } from '@/api/login'
import { getRouterInfo } from '@/api/perm'
import { super_group } from '@/config'

const user = {
  state: {
    token: localStorage.getItem('token'),
    username: localStorage.getItem('username'),
    groups: [],
    menus: undefined,
    eleemnts: undefined,
    permissionMenus: undefined,
    role: ''
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
    SET_ROLE: (state, role) => {
      state.role = role
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
          const cur_date = new Date().getTime()
          localStorage.setItem('token_time', cur_date)
          commit('SET_TOKEN', response.data.token)
          commit('SET_USERNAME', userInfo.username)
          localStorage.setItem('username', userInfo.username)
          localStorage.setItem('token', response.data.token)
          commit('SET_MENUS', undefined)
          commit('SET_ELEMENTS', undefined)
          resolve()
        }).catch(error => {
          reject(error)
        })
      })
    },

    // 获取用户信息
    GetUserInfo({ commit, state }) {
      return new Promise((resolve, reject) => {
        getRouterInfo(state.username).then(response => {
          const data = response.data
          const groups = data.groups
          commit('SET_GROUPS', groups)
          localStorage.setItem('groups', groups)
          if (groups.indexOf(super_group) >= 0) {
            commit('SET_ROLE', 'super')
          } else if (groups.indexOf('OMS_Dev_Manager') >= 0) {
            commit('SET_ROLE', 'devmanager')
          } else if (groups.indexOf('OMS_Test_Manager') >= 0) {
            commit('SET_ROLE', 'testmanager')
          } else if (groups.indexOf('Tb_Development') >= 0) {
            commit('SET_ROLE', 'dev')
          } else {
            commit('SET_ROLE', 'user')
          }
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
          resolve(response)
        }).catch(error => {
          console.log(error)
          reject(error)
        })
      })
    },

    // 登出
    LogOut({ commit, state }) {
      return new Promise((resolve, reject) => {
        logout(state.token).then(() => {
          commit('SET_TOKEN', '')
          localStorage.removeItem('token')
          commit('SET_GROUPS', [])
          localStorage.setItem('groups', [])
          commit('SET_MENUS', undefined)
          commit('SET_ROLE', '')
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
        localStorage.removeItem('token')
        commit('SET_GROUPS', [])
        localStorage.setItem('groups', [])
        commit('SET_MENUS', undefined)
        commit('SET_ROLE', '')
        commit('SET_ELEMENTS', undefined)
        commit('SET_PERMISSION_MENUS', undefined)
        resolve()
      })
    },

    // 动态修改权限
    ChangeRole({ commit, state }, groups) {
      return new Promise(resolve => {
        commit('SET_TOKEN', groups)
        localStorage.setItem('groups', groups)
        getUserInfo(state.username).then(response => {
          const data = response.data.results[0]
          commit('SET_GROUPS', data.groups)
          localStorage.setItem('groups', data.groups)
          resolve()
        })
      })
    }
  }
}

export default user
