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
    url: apiURL.projecttypes + id + '/',
    method: 'delete'
  })
}

// projectenclosures
export function postProjectEnclosure(data) {
  return request({
    url: apiURL.projectenclosures,
    method: 'post',
    data
  })
}

export function getProjectEnclosure(query) {
  return request({
    url: apiURL.projectenclosures,
    method: 'get',
    params: query
  })
}

export function deleteProjectEnclosure(id) {
  return request({
    url: apiURL.projectenclosures + id + '/',
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

// bugmanagers
export function postBugManager(data) {
  return request({
    url: apiURL.bugmanagers,
    method: 'post',
    data
  })
}

export function getBugManager(query) {
  return request({
    url: apiURL.bugmanagers,
    method: 'get',
    params: query
  })
}

export function putBugManager(id, data) {
  return request({
    url: apiURL.bugmanagers + id + '/',
    method: 'put',
    data
  })
}

export function patchBugManager(id, data) {
  return request({
    url: apiURL.bugmanagers + id + '/',
    method: 'patch',
    data
  })
}

export function deleteBugManager(id) {
  return request({
    url: apiURL.bugmanagers + id + '/',
    method: 'delete'
  })
}

// testmanagers
export function postTestManager(data) {
  return request({
    url: apiURL.testmanagers,
    method: 'post',
    data
  })
}

export function getTestManager(query) {
  return request({
    url: apiURL.testmanagers,
    method: 'get',
    params: query
  })
}

export function putTestManager(id, data) {
  return request({
    url: apiURL.testmanagers + id + '/',
    method: 'put',
    data
  })
}

export function deleteTestManager(id) {
  return request({
    url: apiURL.testmanagers + id + '/',
    method: 'delete'
  })
}

// demandmanagers
export function postDemandManager(data) {
  return request({
    url: apiURL.demandmanagers,
    method: 'post',
    data
  })
}

export function getDemandManager(query) {
  return request({
    url: apiURL.demandmanagers,
    method: 'get',
    params: query
  })
}

export function putDemandManager(id, data) {
  return request({
    url: apiURL.demandmanagers + id + '/',
    method: 'put',
    data
  })
}

export function patchDemandManager(id, data) {
  return request({
    url: apiURL.demandmanagers + id + '/',
    method: 'patch',
    data
  })
}

export function deleteDemandManager(id) {
  return request({
    url: apiURL.demandmanagers + id + '/',
    method: 'delete'
  })
}

// demandenclosures
export function postDemandEnclosure(data) {
  return request({
    url: apiURL.demandenclosures,
    method: 'post',
    data
  })
}

export function getDemandEnclosure(query) {
  return request({
    url: apiURL.demandenclosures,
    method: 'get',
    params: query
  })
}

export function deleteDemandEnclosure(id) {
  return request({
    url: apiURL.demandenclosures + id + '/',
    method: 'delete'
  })
}
