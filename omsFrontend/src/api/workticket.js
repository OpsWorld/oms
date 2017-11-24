import fetch from 'utils/fetch';
import apiURL from '@/config'

//worktickets
export function postWorkticket(data) {
    console.log(data)
    return fetch({
        url: apiURL.worktickers,
        method: 'post',
        data
    });
}
export function getWorkticket(query) {
    return fetch({
        url: apiURL.worktickers,
        method: 'get',
        params: query
    });
}

export function putWorkticket(id, data) {
    return fetch({
        url: apiURL.worktickers + id + '/',
        method: 'put',
        data
    });
}

export function deleteWorkticket(id) {
    return fetch({
        url: apiURL.worktickers + id,
        method: 'delete',
    });
}

//tickettypes
export function postTickettype(data) {
    return fetch({
        url: apiURL.tickettypes,
        method: 'post',
        data
    });
}
export function getTickettype(query) {
    return fetch({
        url: apiURL.tickettypes,
        method: 'get',
        params: query
    });
}

export function putTickettype(id, data) {
    return fetch({
        url: apiURL.tickettypes + id + '/',
        method: 'put',
        data
    });
}

export function deleteTickettype(id) {
    return fetch({
        url: apiURL.tickettypes + id,
        method: 'delete',
    });
}