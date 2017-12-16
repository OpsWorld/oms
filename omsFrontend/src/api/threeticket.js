import request from '@/utils/request'
import apiURL from '@/config'

// platforms
export function postPlatform(data) {
  return request({
    url: apiURL.platforms,
    method: 'post',
    data
  })
}

export function getPlatform(query) {
  return request({
    url: apiURL.platforms,
    method: 'get',
    params: query
  })
}

export function putPlatform(id, data) {
  return request({
    url: apiURL.platforms + id + '/',
    method: 'put',
    data
  })
}

export function deletePlatform(id) {
  return request({
    url: apiURL.platforms + id + '/',
    method: 'delete'
  })
}

// merchants
export function postMerchant(data) {
  return request({
    url: apiURL.merchants,
    method: 'post',
    data
  })
}

export function getMerchant(query) {
  return request({
    url: apiURL.merchants,
    method: 'get',
    params: query
  })
}

export function putMerchant(id, data) {
  return request({
    url: apiURL.merchants + id + '/',
    method: 'put',
    data
  })
}

export function deleteMerchant(id) {
  return request({
    url: apiURL.merchants + id + '/',
    method: 'delete'
  })
}

// platformenclosures
export function postPlatformEnclosure(data) {
  return request({
    url: apiURL.platformenclosures,
    method: 'post',
    data
  })
}

export function getPlatformEnclosure(query) {
  return request({
    url: apiURL.platformenclosures,
    method: 'get',
    params: query
  })
}

export function putPlatformEnclosure(id, data) {
  return request({
    url: apiURL.platformenclosures + id + '/',
    method: 'put',
    data
  })
}

export function deletePlatformEnclosure(id) {
  return request({
    url: apiURL.platformenclosures + id + '/',
    method: 'delete'
  })
}

// threepaytickets
export function postThreepayTicket(data) {
  return request({
    url: apiURL.threepaytickets,
    method: 'post',
    data
  })
}

export function getThreepayTicket(query) {
  return request({
    url: apiURL.threepaytickets,
    method: 'get',
    params: query
  })
}

export function putThreepayTicket(id, data) {
  return request({
    url: apiURL.threepaytickets + id + '/',
    method: 'put',
    data
  })
}

export function deleteThreepayTicket(id) {
  return request({
    url: apiURL.threepaytickets + id + '/',
    method: 'delete'
  })
}
