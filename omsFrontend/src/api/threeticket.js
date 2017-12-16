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

// threepayenclosures
export function postThreepayEnclosure(data) {
  return request({
    url: apiURL.threepayenclosures,
    method: 'post',
    data
  })
}

export function getThreepayEnclosure(query) {
  return request({
    url: apiURL.threepayenclosures,
    method: 'get',
    params: query
  })
}

export function putThreepayEnclosure(id, data) {
  return request({
    url: apiURL.threepayenclosures + id + '/',
    method: 'put',
    data
  })
}

export function deleteThreepayEnclosure(id) {
  return request({
    url: apiURL.threepayenclosures + id + '/',
    method: 'delete'
  })
}
