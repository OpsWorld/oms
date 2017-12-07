import fetch from 'utils/fetch';
import apiURL from '@/config'

//upload
export function postMenuPerm(data) {
    return fetch({
        url: apiURL.usermenuperms,
        method: 'post',
        data
    });
}

export function getMenuPerm(query, id) {
    return fetch({
        url: apiURL.usermenuperms,
        method: 'get',
        params: query
    });
}

export function putMenuPerm(id, data) {
    return fetch({
        url: apiURL.usermenuperms + id + '/',
        method: 'put',
        data
    });
}

export function deleteMenuPerm(id) {
    return fetch({
        url: apiURL.usermenuperms + id,
        method: 'delete',
    });
}

// routers
export function getRouters() {
    return fetch({
        url: apiURL.routers,
        method: 'get',
    });
}