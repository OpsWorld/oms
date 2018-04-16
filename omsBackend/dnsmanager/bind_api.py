# -*- coding: utf-8 -*-
# author: itimor

from __future__ import unicode_literals
import requests
import json
import urllib.parse


class ApiError(Exception):
    """
    错误类，用于对外显示错误信息
    """

    def __init__(self, error_code, error_message):
        super(ApiError, self).__init__()
        self.error_code = int(error_code)
        self.error_message = error_message


class BindApi(object):
    def __init__(self, user=None, pwd=None, token=None):
        # 用户配置数据
        self.user = user
        self.pwd = pwd
        self.token = token
        self.headers = {
            "Content-type": "application/x-www-form-urlencoded",
            'User-Agent': 'itimor@126.com',
        }

        # url
        self.API_URL = 'http://127.0.0.1:8888/api/'
        self.DOMAIN_URL = self.API_URL + 'domains/'
        self.RECORD_URL = self.API_URL + 'records/'

    def get_token(self):
        pam = {'username': self.user, 'password': self.pwd}
        suffix_url = 'api-token-auth/'
        url = self.API_URL + suffix_url
        req = requests.post(url, data=pam, headers=self.headers)
        token = json.loads(req.text)['token']
        return token

    def auth_header(self):
        """生成公共 通用参数部分"""
        if self.token is None:
            self.token = self.get_token()

        pam = {'Authorization': 'token ' + self.token}
        self.headers.update(pam)
        return pam

    def get_response(self, url, method, param_data=None):
        """
        将 方法,基础url,参数合并成 url请求,并向服务器发送获取结果然后返回
        """
        self.auth_header()
        if method == 'get':
            params = None
            if param_data:
                params = urllib.parse.urlencode(param_data)
            reader = requests.get(url, params, headers=self.headers)
        elif method == 'post':
            reader = requests.post(url, data=param_data, headers=self.headers)
        else:
            reader = requests.put(url, data=param_data, headers=self.headers)

        msg = reader.text
        return msg

    def get_domains(self):
        method = 'get'
        ret_json = self.get_response(self.DOMAIN_URL, method)
        req = json.loads(ret_json, encoding='utf-8')
        return req

    def get_domain_id(self, domain):
        method = 'get'
        param_data = {'name': domain}
        ret_json = self.get_response(self.DOMAIN_URL, method, param_data)
        req = json.loads(ret_json, encoding='utf-8')[0]['id']
        return req

    def add_domain(self, domain):
        method = 'post'
        data = {'name': domain}
        ret_json = self.get_response(self.DOMAIN_URL, method, param_data=data)
        req = json.loads(ret_json, encoding='utf-8')
        return req

    def get_records(self, domain):
        method = 'get'
        param_data = {'domain__name': domain}
        ret_json = self.get_response(self.RECORD_URL, method, param_data)
        req = json.loads(ret_json, encoding='utf-8')
        return req

    def add_record(self, domain, record, value, type='A', ttl=600):
        method = 'post'
        title = '{}-{}-{}-{}'.format(domain, record, value, type)
        data = {'title': title, 'domain': domain, 'name': record, 'value': value, 'type': type, 'ttl': ttl}
        ret_json = self.get_response(self.RECORD_URL, method, param_data=data)
        req = json.loads(ret_json, encoding='utf-8')
        return req

    def update_record(self, record_id, domain, record, value, type='A', ttl=600):
        method = 'put'
        data = {'domain': domain, 'name': record, 'value': value, 'type': type, 'ttl': ttl}
        ret_json = self.get_response(self.RECORD_URL + str(record_id) + '/', method, param_data=data)
        req = json.loads(ret_json, encoding='utf-8')
        return req

if __name__ == '__main__':
    from dnsapi_key import BIND_KEYINFO

    bindapi = BindApi(user=BIND_KEYINFO['user'], pwd=BIND_KEYINFO['pwd'])
    data = {'name': 'itimor.ph'}
    print(bindapi.get_domains())
