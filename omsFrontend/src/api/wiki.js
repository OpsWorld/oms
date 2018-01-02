import request from '@/utils/request'
import apiURL from '@/config'

// wikis
export function postWiki(data) {
  return request({
    url: apiURL.wikis,
    method: 'post',
    data
  })
}

export function getWiki(query, id) {
  return request({
    url: id ? apiURL.wikis + id + '/' : apiURL.wikis,
    method: 'get',
    params: query
  })
}

export function putWiki(id, data) {
  return request({
    url: apiURL.wikis + id + '/',
    method: 'put',
    data
  })
}

export function deleteWiki(id) {
  return request({
    url: apiURL.wikis + id + '/',
    method: 'delete'
  })
}
