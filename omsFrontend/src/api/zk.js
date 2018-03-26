import request from '@/utils/request'
import zkapiUrl from '@/config'

// zkusers
export function getzkUser(query) {
  return request({
    url: zkapiUrl.zkusers,
    method: 'get',
    params: query
  })
}

export function deletezkUser(id, data) {
  return request({
    url: zkapiUrl.zkusers + id + '/',
    method: 'delete',
    data
  })
}

// zkpunchs
export function getzkPunch(query) {
  return request({
    url: zkapiUrl.zkpunchs,
    method: 'get',
    params: query
  })
}

export function deletezkPunch(id, data) {
  return request({
    url: zkapiUrl.zkpunchs + id + '/',
    method: 'delete',
    data
  })
}
