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
  return request({
    url: id ? apiURL.uploads + id + '/' : apiURL.uploads,
    method: 'get',
    params: query
  })
}

export function deleteUpload(id) {
  return request({
    url: apiURL.uploads + id + '/',
    method: 'delete'
  })
}

// sendmail
export function postSendmail(data) {
  return request({
    url: apiURL.sendmail,
    method: 'post',
    data
  })
}

// sendmessage
export function postSendmessage(data) {
  return request({
    url: apiURL.sendmessage,
    method: 'post',
    data
  })
}

export function getSendmessage(query, id) {
  return request({
    url: id ? apiURL.sendmessage + id + '/' : apiURL.sendmessage,
    method: 'get',
    params: query
  })
}

export function deleteSendmessage(id) {
  return request({
    url: apiURL.sendmessage + id + '/',
    method: 'delete'
  })
}
