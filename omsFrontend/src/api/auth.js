import fetch from 'utils/fetch';
import apiURL from '@/config'

export function login(data) {
  return fetch({
    url: apiURL.login,
    method: 'post',
    data
  });
}

export function logout() {
  return "logout"
}

export function getInfo(username) {
  return fetch({
    url: apiURL.users,
    method: 'get',
    params: {
      username
    }
  });
}


//password
export function changePassword(data) {
    return fetch({
        url: apiURL.changePassword,
        method: 'post',
        data
    })
}