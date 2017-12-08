import request from '@/utils/request'
import apiURL from '@/config'

// worktickets
export function postWorkticket(data) {
  console.log(data)
  return request({
    url: apiURL.worktickers,
    method: 'post',
    data
  })
}

export function getWorkticket(id, query) {
  return request({
    url: id ? apiURL.worktickers + id + '/' : apiURL.worktickers,
    method: 'get',
    params: query
  })
}

export function putWorkticket(id, data) {
  return request({
    url: apiURL.worktickers + id + '/',
    method: 'put',
    data
  })
}

export function patchWorkticket(id, data) {
  return request({
    url: apiURL.worktickers + id + '/',
    method: 'patch',
    data
  })
}

export function deleteWorkticket(id) {
  return request({
    url: apiURL.worktickers + id,
    method: 'delete'
  })
}

// tickettypes
export function postTickettype(data) {
  return request({
    url: apiURL.tickettypes,
    method: 'post',
    data
  })
}

export function getTickettype(query) {
  return request({
    url: apiURL.tickettypes,
    method: 'get',
    params: query
  })
}

export function putTickettype(id, data) {
  return request({
    url: apiURL.tickettypes + id + '/',
    method: 'put',
    data
  })
}

export function deleteTickettype(id) {
  return request({
    url: apiURL.tickettypes + id,
    method: 'delete'
  })
}

// ticketcomments
export function postTicketcomment(data) {
  return request({
    url: apiURL.ticketcomments,
    method: 'post',
    data
  })
}

export function getTicketcomment(query) {
  return request({
    url: apiURL.ticketcomments,
    method: 'get',
    params: query
  })
}

export function putTicketcomment(id, data) {
  return request({
    url: apiURL.ticketcomments + id + '/',
    method: 'put',
    data
  })
}

export function deleteTicketcomment(id) {
  return request({
    url: apiURL.ticketcomments + id,
    method: 'delete'
  })
}

// ticketenclosures
export function postTicketenclosure(data) {
  return request({
    url: apiURL.ticketenclosures,
    method: 'post',
    data
  })
}

export function getTicketenclosure(query) {
  return request({
    url: apiURL.ticketenclosures,
    method: 'get',
    params: query
  })
}

export function deleteTicketenclosure(id) {
  return request({
    url: apiURL.ticketenclosures + id,
    method: 'delete'
  })
}
