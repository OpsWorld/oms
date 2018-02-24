import request from '@/utils/request'
import apiURL from '@/config'

// opsprojects
export function postProject(data) {
  return request({
    url: apiURL.opsprojects,
    method: 'post',
    data
  })
}

export function getProject(query, id) {
  return request({
    url: id ? apiURL.opsprojects + id + '/' : apiURL.opsprojects,
    method: 'get',
    params: query
  })
}

export function putProject(id, data) {
  return request({
    url: apiURL.opsprojects + id + '/',
    method: 'put',
    data
  })
}

export function patchProject(id, data) {
  return request({
    url: apiURL.opsprojects + id + '/',
    method: 'patch',
    data
  })
}

export function deleteProject(id) {
  return request({
    url: apiURL.opsprojects + id + '/',
    method: 'delete'
  })
}

// opsprojecttypes
export function postProjectType(data) {
  return request({
    url: apiURL.opsprojecttypes,
    method: 'post',
    data
  })
}

export function getProjectType(query) {
  return request({
    url: apiURL.opsprojecttypes,
    method: 'get',
    params: query
  })
}

export function putProjectType(id, data) {
  return request({
    url: apiURL.opsprojecttypes + id + '/',
    method: 'put',
    data
  })
}

export function deleteProjectType(id) {
  return request({
    url: apiURL.opsprojecttypes + id + '/',
    method: 'delete'
  })
}

// opsprojectenclosures
export function postProjectEnclosure(data) {
  return request({
    url: apiURL.opsprojectenclosures,
    method: 'post',
    data
  })
}

export function getProjectEnclosure(query) {
  return request({
    url: apiURL.opsprojectenclosures,
    method: 'get',
    params: query
  })
}

export function deleteProjectEnclosure(id) {
  return request({
    url: apiURL.opsprojectenclosures + id + '/',
    method: 'delete'
  })
}

// opsdemandmanagers
export function postopsDemandManager(data) {
  return request({
    url: apiURL.opsdemandmanagers,
    method: 'post',
    data
  })
}

export function getDemandManager(query) {
  return request({
    url: apiURL.opsdemandmanagers,
    method: 'get',
    params: query
  })
}

export function putDemandManager(id, data) {
  return request({
    url: apiURL.opsdemandmanagers + id + '/',
    method: 'put',
    data
  })
}

export function patchDemandManager(id, data) {
  return request({
    url: apiURL.opsdemandmanagers + id + '/',
    method: 'patch',
    data
  })
}

export function deleteDemandManager(id) {
  return request({
    url: apiURL.opsdemandmanagers + id + '/',
    method: 'delete'
  })
}

// opsdemandenclosures
export function postopsDemandEnclosure(data) {
  return request({
    url: apiURL.opsdemandenclosures,
    method: 'post',
    data
  })
}

export function getDemandEnclosure(query) {
  return request({
    url: apiURL.opsdemandenclosures,
    method: 'get',
    params: query
  })
}

export function deleteDemandEnclosure(id) {
  return request({
    url: apiURL.opsdemandenclosures + id + '/',
    method: 'delete'
  })
}
