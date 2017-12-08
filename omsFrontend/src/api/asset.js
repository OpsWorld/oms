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

export function getHostList(query) {
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

export function deleteHost(id) {
  return request({
    url: apiURL.hosts + id,
    method: 'delete'
  })
}

// jobgroups
export function postHostGroup(data) {
  return request({
    url: apiURL.hostgroups,
    method: 'post',
    data
  })
}

export function getHostGroupList(query) {
  return request({
    url: apiURL.hostgroups,
    method: 'get',
    params: query
  })
}

export function putHostGroup(id, data) {
  return request({
    url: apiURL.hostgroups + id + '/',
    method: 'put',
    data
  })
}

export function deleteHostGroup(id) {
  return request({
    url: apiURL.hostgroups + id,
    method: 'delete'
  })
}
