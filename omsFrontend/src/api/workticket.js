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

export function getWorkticket(id,query) {
    return fetch({
        url: id?apiURL.worktickers + id + '/':apiURL.worktickers,
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

//ticketcomments
export function postTicketcomment(data) {
    return fetch({
        url: apiURL.ticketcomments,
        method: 'post',
        data
    });
}
export function getTicketcomment(query) {
    return fetch({
        url: apiURL.ticketcomments,
        method: 'get',
        params: query
    });
}

export function putTicketcomment(id, data) {
    return fetch({
        url: apiURL.ticketcomments + id + '/',
        method: 'put',
        data
    });
}

export function deleteTicketcomment(id) {
    return fetch({
        url: apiURL.ticketcomments + id,
        method: 'delete',
    });
}