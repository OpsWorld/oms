import request from '@/utils/request'
import apiURL from '@/config'

// salts
export function getAllminions() {
  return request({
    url: apiURL.get_all_key,
    method: 'get'
  })
}

export function getAllminionStatus() {
  return request({
    url: apiURL.minions_status,
    method: 'get'
  })
}

export function getMinionInfo(key_id) {
  return request({
    url: apiURL.get_minion_info + key_id,
    method: 'get'
  })
}

export function getCmdrun(data) {
  return request({
    url: apiURL.cmdrun,
    method: 'post',
    data
  })
}

export function getSaltResult(jid) {
  return request({
    url: apiURL.get_result + jid,
    method: 'get'
  })
}

export function getSyncRemoteServer(method) {
  return request({
    url: apiURL.sync_remote_server + method,
    method: 'get'
  })
}
