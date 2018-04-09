import request from '@/utils/request'
import apiURL from '@/config'

// dnsapikeys
export function postDnsapiKey(data) {
  return request({
    url: apiURL.dnsapikeys,
    method: 'post',
    data
  })
}

export function getDnsapiKey(query) {
  return request({
    url: apiURL.dnsapikeys,
    method: 'get',
    params: query
  })
}

export function putDnsapiKey(id, data) {
  return request({
    url: apiURL.dnsapikeys + id + '/',
    method: 'put',
    data
  })
}

export function deleteDnsapiKey(id) {
  return request({
    url: apiURL.dnsapikeys + id + '/',
    method: 'delete'
  })
}

// dnspoddomains
export function getDnspodDomain(query) {
  return request({
    url: apiURL.dnspoddomains,
    method: 'get',
    params: query
  })
}

// godaddydomains
export function getGodaddyDomain(query) {
  return request({
    url: apiURL.godaddydomains,
    method: 'get',
    params: query
  })
}

// dnspodrecords
export function postDnspodRecord(data) {
  return request({
    url: apiURL.dnspodrecords,
    method: 'post',
    data
  })
}

export function getDnspodRecord(query) {
  return request({
    url: apiURL.dnspodrecords,
    method: 'get',
    params: query
  })
}

// godaddyreecords
export function postGodaddyRecord(data) {
  return request({
    url: apiURL.godaddyreecords,
    method: 'post',
    data
  })
}

export function getGodaddyRecord(query) {
  return request({
    url: apiURL.godaddyreecords,
    method: 'get',
    params: query
  })
}

// dnsdomains
export function getDnsDomain(query) {
  return request({
    url: apiURL.dnsdomains,
    method: 'get',
    params: query
  })
}

// dnsrecords
export function getDnsRecord(query) {
  return request({
    url: apiURL.dnsrecords,
    method: 'get',
    params: query
  })
}
