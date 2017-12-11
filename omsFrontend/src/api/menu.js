import request from '@/utils/request'
import apiURL from '@/config'

// firstmenus
export function postFirstmenus(data) {
  return request({
    url: apiURL.firstmenus,
    method: 'post',
    data
  })
}

export function getFirstmenus(query, id) {
  return request({
    url: id ? apiURL.firstmenus + id + '/' : apiURL.firstmenus,
    method: 'get',
    params: query
  })
}

export function putFirstmenus(id, data) {
  return request({
    url: apiURL.firstmenus + id + '/',
    method: 'put',
    data
  })
}

export function deleteFirstmenus(id) {
  return request({
    url: apiURL.firstmenus + id,
    method: 'delete'
  })
}

// secondmenus
export function postSecondmenus(data) {
  return request({
    url: apiURL.secondmenus,
    method: 'post',
    data
  })
}

export function getSecondmenus(query, id) {
  return request({
    url: id ? apiURL.secondmenus + id + '/' : apiURL.secondmenus,
    method: 'get',
    params: query
  })
}

export function putSecondmenus(id, data) {
  return request({
    url: apiURL.secondmenus + id + '/',
    method: 'put',
    data
  })
}

export function deleteSecondmenus(id) {
  return request({
    url: apiURL.secondmenus + id,
    method: 'delete'
  })
}

// menumetas
export function postMenumetas(data) {
  console.log(data)
  return request({
    url: apiURL.menumetas,
    method: 'post',
    data
  })
}

export function getMenumetas(query, id) {
  return request({
    url: id ? apiURL.menumetas + id + '/' : apiURL.menumetas,
    method: 'get',
    params: query
  })
}

export function putMenumetas(id, data) {
  return request({
    url: apiURL.menumetas + id + '/',
    method: 'put',
    data
  })
}

export function deleteMenumetas(id) {
  return request({
    url: apiURL.menumetas + id,
    method: 'delete'
  })
}
