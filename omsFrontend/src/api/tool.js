import request from '@/utils/request'
import apiURL from '@/config'

// upload
export function postUpload(data) {
  return request({
    url: apiURL.uploads,
    method: 'post',
    data
  })
}

export function getUploadList(query, id) {
  if (query.time_lte === 'NaN-aN-aN' || query.time_lte === '1970-01-01') {
    delete query.time_gte
    delete query.time_lte
  }
  return request({
    url: id ? apiURL.uploads + id + '/' : apiURL.uploads,
    method: 'get',
    params: query
  })
}

export function putUpload(id, data) {
  return request({
    url: apiURL.uploads + id + '/',
    method: 'put',
    data
  })
}

export function deleteUpload(id) {
  return request({
    url: apiURL.uploads + id,
    method: 'delete'
  })
}
