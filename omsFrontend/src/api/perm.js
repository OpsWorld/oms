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

// userwikiperms
export function postWikiPerm(data) {
  return request({
    url: apiURL.userwikiperms,
    method: 'post',
    data
  })
}

export function getWikiPerm(query, id) {
  return request({
    url: apiURL.userwikiperms,
    method: 'get',
    params: query
  })
}

export function putWikiPerm(id, data) {
  return request({
    url: apiURL.userwikiperms + id + '/',
    method: 'put',
    data
  })
}

export function deleteWikiPerm(id) {
  return request({
    url: apiURL.userwikiperms + id + '/',
    method: 'delete'
  })
}
