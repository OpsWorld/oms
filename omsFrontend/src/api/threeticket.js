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

// paychannelnames
export function postPayChannelName(data) {
  return request({
    url: apiURL.paychannelnames,
    method: 'post',
    data
  })
}

export function getPayChannelName(query) {
  return request({
    url: apiURL.paychannelnames,
    method: 'get',
    params: query
  })
}

export function putPayChannelName(id, data) {
  return request({
    url: apiURL.paychannelnames + id + '/',
    method: 'put',
    data
  })
}

export function deletePayChannelName(id) {
  return request({
    url: apiURL.paychannelnames + id + '/',
    method: 'delete'
  })
}

// paychannels
export function postPayChannel(data) {
  console.log(data)
  return request({
    url: apiURL.paychannels,
    method: 'post',
    data
  })
}

export function getPayChannel(query) {
  return request({
    url: apiURL.paychannels,
    method: 'get',
    params: query
  })
}

export function putPayChannel(id, data) {
  return request({
    url: apiURL.paychannels + id + '/',
    method: 'put',
    data
  })
}

export function deletePayChannel(id) {
  return request({
    url: apiURL.paychannels + id + '/',
    method: 'delete'
  })
}

// threepayenclosures
export function postThreePayEnclosure(data) {
  return request({
    url: apiURL.threepayenclosures,
    method: 'post',
    data
  })
}

export function getThreePayEnclosure(query) {
  return request({
    url: apiURL.threepayenclosures,
    method: 'get',
    params: query
  })
}

export function putThreePayEnclosure(id, data) {
  return request({
    url: apiURL.threepayenclosures + id + '/',
    method: 'put',
    data
  })
}

export function deleteThreePayEnclosure(id) {
  return request({
    url: apiURL.threepayenclosures + id + '/',
    method: 'delete'
  })
}
