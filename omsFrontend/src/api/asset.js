import fetch from 'utils/fetch';
import apiURL from '@/config'

//hosts
export function postHost(data) {
    return fetch({
        url: apiURL.hosts,
        method: 'post',
        data
    });
}
export function getHostList(query) {
    return fetch({
        url: apiURL.hosts,
        method: 'get',
        params: query
    });
}

export function putHost(id, data) {
    console.log(data);
    return fetch({
        url: apiURL.hosts + id + '/',
        method: 'put',
        data
    });
}

export function deleteHost(id) {
    return fetch({
        url: apiURL.hosts + id,
        method: 'delete',
    });
}


// jobgroups
export function postHostGroup(data) {
    return fetch({
        url: apiURL.hostgroups,
        method: 'post',
        data
    });
}

export function getHostGroupList(query) {
    return fetch({
        url: apiURL.hostgroups,
        method: 'get',
        params: query
    });
}

export function putHostGroup(id, data) {
    return fetch({
        url: apiURL.hostgroups + id + '/',
        method: 'put',
        data
    });
}

export function deleteHostGroup(id) {
    return fetch({
        url: apiURL.hostgroups + id,
        method: 'delete',
    });
}