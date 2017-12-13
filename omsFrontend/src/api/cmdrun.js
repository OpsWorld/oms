import request from '@/utils/request'
import apiURL from '@/config'

// upload
export function postCmdrun(data) {
  return request({
    url: apiURL.cmdrun,
    method: 'post',
    data
  })
}

export function getCmdrun(query, id) {
  return request({
    url: id ? apiURL.cmdrun + id + '/' : apiURL.cmdrun,
    method: 'get',
    params: query
  })
}

export function putCmdrun(id, data) {
  return request({
    url: apiURL.cmdrun + id + '/',
    method: 'put',
    data
  })
}

export function deleteCmdrun(id) {
  return request({
    url: apiURL.cmdrun + id,
    method: 'delete'
  })
}
