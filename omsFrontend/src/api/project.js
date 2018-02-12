import request from '@/utils/request'
import apiURL from '@/config'

// projects
export function postProject(data) {
  return request({
    url: apiURL.projects,
    method: 'post',
    data
  })
}

export function getProject(query, id) {
  return request({
    url: id ? apiURL.projects + id + '/' : apiURL.projects,
    method: 'get',
    params: query
  })
}

export function putProject(id, data) {
  return request({
    url: apiURL.projects + id + '/',
    method: 'put',
    data
  })
}

export function patchProject(id, data) {
  return request({
    url: apiURL.projects + id + '/',
    method: 'patch',
    data
  })
}

export function deleteProject(id) {
  return request({
    url: apiURL.projects + id + '/',
    method: 'delete'
  })
}

// projecttypes
export function postProjectType(data) {
  return request({
    url: apiURL.projecttypes,
    method: 'post',
    data
  })
}

export function getProjectType(query) {
  return request({
    url: apiURL.projecttypes,
    method: 'get',
    params: query
  })
}

export function putProjectType(id, data) {
  return request({
    url: apiURL.projecttypes + id + '/',
    method: 'put',
    data
  })
}

export function deleteProjectType(id) {
  return request({
    url: apiURL.tickettypes + id + '/',
    method: 'delete'
  })
}

// projectcomments
export function postProjectComment(data) {
  return request({
    url: apiURL.projectcomments,
    method: 'post',
    data
  })
}

export function getProjectComment(query) {
  return request({
    url: apiURL.projectcomments,
    method: 'get',
    params: query
  })
}

export function putProjectComment(id, data) {
  return request({
    url: apiURL.projectcomments + id + '/',
    method: 'put',
    data
  })
}

export function deleteProjectComment(id) {
  return request({
    url: apiURL.projectcomments + id + '/',
    method: 'delete'
  })
}
