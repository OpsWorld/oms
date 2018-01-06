import request from '@/utils/request'
import apiURL from '@/config'

// jobs
export function postJob(data) {
  return request({
    url: apiURL.jobs,
    method: 'post',
    data
  })
}

export function getJob(query) {
  return request({
    url: apiURL.jobs,
    method: 'get',
    params: query
  })
}

export function putJob(id, data) {
  return request({
    url: apiURL.jobs + id + '/',
    method: 'put',
    data
  })
}

export function deleteJob(id) {
  return request({
    url: apiURL.jobs + id + '/',
    method: 'delete'
  })
}

// deployenvs
export function postDeployenv(data) {
  return request({
    url: apiURL.deployenvs,
    method: 'post',
    data
  })
}

export function getDeployenv(query) {
  return request({
    url: apiURL.deployenvs,
    method: 'get',
    params: query
  })
}

export function putDeployenv(id, data) {
  return request({
    url: apiURL.deployenvs + id + '/',
    method: 'put',
    data
  })
}

export function deleteDeployenv(id) {
  return request({
    url: apiURL.deployenvs + id + '/',
    method: 'delete'
  })
}

// deployjobs
export function postDeployJob(data) {
  return request({
    url: apiURL.deployjobs,
    method: 'post',
    data
  })
}

export function getDeployJob(query) {
  return request({
    url: apiURL.deployjobs,
    method: 'get',
    params: query
  })
}
