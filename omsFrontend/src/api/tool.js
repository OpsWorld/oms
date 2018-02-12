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

export function getUpload(query, id) {
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

// calenders
export function postCalender(data) {
  return request({
    url: apiURL.calenders,
    method: 'post',
    data
  })
}

export function getCalender(query, id) {
  return request({
    url: id ? apiURL.calenders + id + '/' : apiURL.calenders,
    method: 'get',
    params: query
  })
}

export function deleteCalender(id) {
  return request({
    url: apiURL.calenders + id + '/',
    method: 'delete'
  })
}

// records
export function postRecord(data) {
  return request({
    url: apiURL.records,
    method: 'post',
    data
  })
}

export function getRecord(query, id) {
  return request({
    url: apiURL.records,
    method: 'get',
    params: query
  })
}
