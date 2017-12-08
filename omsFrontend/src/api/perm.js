import request from '@/utils/request'
import apiURL from '@/config'

// upload
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
    url: apiURL.usermenuperms + id,
    method: 'delete'
  })
}

// router
export function getRouterInfo(query) {
  return request({
    url: apiURL.routerinfo,
    method: 'get',
    params: query
  })
}
