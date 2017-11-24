import fetch from 'utils/fetch';
import apiURL from '@/config'

//users
export function postUser(data) {
    return fetch({
        url: apiURL.users,
        method: 'post',
        data
    });
}
export function getUserList(query) {
    return fetch({
        url: apiURL.users,
        method: 'get',
        params: query
    });
}

export function patchUser(id, data) {
    console.log(data);
    return fetch({
        url: apiURL.users + id + '/',
        method: 'patch',
        data
    });
}

export function deleteUser(id) {
    return fetch({
        url: apiURL.users + id,
        method: 'delete',
    });
}


//groups
export function postGroup(data) {
    console.log(data);
    return fetch({
        url: apiURL.groups,
        method: 'post',
        data
    });
}

export function getGroupList(query) {
    return fetch({
        url: apiURL.groups,
        method: 'get',
        params: query
    });
}

export function putGroup(id, data) {
    return fetch({
        url: apiURL.groups + id + '/',
        method: 'put',
        data
    });
}

export function deleteGroup(id) {
    return fetch({
        url: apiURL.groups + id,
        method: 'delete',
    });
}

//roles
export function postRole(data) {
    return fetch({
        url: apiURL.roles,
        method: 'post',
        data
    });
}

export function getRoleList(query) {
    return fetch({
        url: apiURL.roles,
        method: 'get',
        params: query
    });
}

export function putRole(id, data) {
    return fetch({
        url: apiURL.roles + id + '/',
        method: 'put',
        data
    });
}

export function deleteRole(id) {
    return fetch({
        url: apiURL.roles + id,
        method: 'delete',
    });
}