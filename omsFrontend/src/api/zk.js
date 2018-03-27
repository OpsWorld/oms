import request from '@/utils/request'
import apiUrl from '@/config'

// zkusers
export function getzkUser(query) {
  return request({
    url: apiUrl.zkusers,
    method: 'get',
    params: query
  })
}

export function deletezkUser(id, data) {
  return request({
    url: apiUrl.zkusers + id + '/',
    method: 'delete',
    data
  })
}

// zkpunchs
export function getzkPunch(query) {
  return request({
    url: apiUrl.zkpunchs,
    method: 'get',
    params: query
  })
}

export function deletezkPunch(id, data) {
  return request({
    url: apiUrl.zkpunchs + id + '/',
    method: 'delete',
    data
  })
}

// zkpunchset
export function postzkPunchSet(data) {
  return request({
    url: apiUrl.zkpunchset,
    method: 'post',
    data
  })
}

export function getzkPunchSet(query) {
  return request({
    url: apiUrl.zkpunchset,
    method: 'get',
    params: query
  })
}

export function putzkPunchSet(id, data) {
  return request({
    url: apiUrl.zkpunchset + id + '/',
    method: 'put',
    data
  })
}

export function deletezkPunchSet(id) {
  return request({
    url: apiUrl.zkpunchset + id + '/',
    method: 'delete'
  })
}
