import request from '@/utils/request'
import apiURL from '@/config'

// usermenuperms
export function postMenuPerm(data) {
  return request({
    url: apiURL.usermenuperms,
    method: 'post',
    data
  })
}

export function getMenuPerm(query, id) {
  return request({
    url: apiURL.usermenuperms,
    method: 'get',
    params: query
  })
}

export function putMenuPerm(id, data) {
  return request({
    url: apiURL.usermenuperms + id + '/',
    method: 'put',
    data
  })
}

export function deleteMenuPerm(id) {
  return request({
    url: apiURL.usermenuperms + id + '/',
    method: 'delete'
  })
}

// router
export function getRouterInfo(username) {
  return request({
    url: apiURL.routerinfo + username,
    method: 'get'
  })
}

// userhostperms
export function postHostPerm(data) {
  return request({
    url: apiURL.userhostperms,
    method: 'post',
    data
  })
}

export function getHostPerm(query, id) {
  return request({
    url: apiURL.userhostperms,
    method: 'get',
    params: query
  })
}

export function putHostPerm(id, data) {
  return request({
    url: apiURL.userhostperms + id + '/',
    method: 'put',
    data
  })
}

export function deleteHostPerm(id) {
  return request({
    url: apiURL.userhostperms + id + '/',
    method: 'delete'
  })
}
