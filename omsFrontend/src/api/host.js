import request from '@/utils/request'
import apiURL from '@/config'

// hosts
export function postHost(data) {
  return request({
    url: apiURL.hosts,
    method: 'post',
    data
  })
}

export function getHost(query) {
  return request({
    url: apiURL.hosts,
    method: 'get',
    params: query
  })
}

export function putHost(id, data) {
  return request({
    url: apiURL.hosts + id + '/',
    method: 'put',
    data
  })
}

export function patchHost(id, data) {
  return request({
    url: apiURL.hosts + id + '/',
    method: 'patch',
    data
  })
}

export function deleteHost(id) {
  return request({
    url: apiURL.hosts + id + '/',
    method: 'delete'
  })
}

// idcs
export function postIdc(data) {
  return request({
    url: apiURL.idcs,
    method: 'post',
    data
  })
}

export function getIdc(query) {
  return request({
    url: apiURL.idcs,
    method: 'get',
    params: query
  })
}

export function putIdc(id, data) {
  return request({
    url: apiURL.idcs + id + '/',
    method: 'put',
    data
  })
}

export function deleteIdc(id) {
  return request({
    url: apiURL.idcs + id + '/',
    method: 'delete'
  })
}
