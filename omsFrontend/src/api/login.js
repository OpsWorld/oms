import request from '@/utils/request'
import apiURL from '@/config'

export function login(data) {
  return request({
    url: apiURL.login,
    method: 'post',
    data
  })
}

export function logout() {
  return request({
    url: apiURL.logout,
    method: 'get'
  })
}

export function getUserInfo(username) {
  const params = {
    username: username
  }
  return request({
    url: apiURL.users,
    method: 'get',
    params: params
  })
}

