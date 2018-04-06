# -*- coding: utf-8 -*-
# author: itimor

from __future__ import unicode_literals
import requests
import json
import logging


def initlog(logfile):
    """
    创建日志实例
    """
    logger = logging.getLogger()
    hdlr = logging.FileHandler(logfile)
    formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')
    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr)
    logger.setLevel(logging.NOTSET)
    return logger


class DnspodApiError(Exception):
    """
    错误类，用于对外显示错误信息
    """

    def __init__(self, error_code, error_message):
        super(DnspodApiError, self).__init__()
        self.error_code = int(error_code)
        self.error_message = error_message


class DnspodApi(object):
    def __init__(self, user=None, pwd=None, token=None, format='json', lang='cn', error_on_empty='no', user_id=None):
        # 用户配置数据
        self.Duser = user
        self.Dpwd = pwd
        self.Dformat = format
        self.Dlang = lang
        self.Derror_on_empty = error_on_empty
        self.Dtoken = token
        self.Duser_id = user_id

        # url
        self.API_DOMAINS = 'https://dnsapi.cn/Domain.'
        self.API_RECORDS = 'https://dnsapi.cn/Record.'

    def auth_param(self):
        """生成公共 通用参数部分"""
        if self.Dtoken is None:
            pam = {'login_email': self.Duser,
                   'login_password': self.Dpwd,
                   'format': self.Dformat,
                   'lang': self.Dlang,
                   'error_on_empty': self.Derror_on_empty}
        else:
            pam = {'login_token': self.Dtoken,
                   'format': self.Dformat,
                   'lang': self.Dlang,
                   'error_on_empty': self.Derror_on_empty}
        if self.Duser_id is not None:
            pam['user_id'] = self.Duser_id
        return pam

    def post_data(self, url, param_data=None):
        """
        将 方法,基础url,参数合并成 url请求,并向服务器发送获取结果然后返回
        """
        user_agent = "itimor@126.com"
        auth_param = self.auth_param()
        if param_data:
            params = dict(auth_param, **param_data)
        else:
            params = auth_param
        header = {'User-Agent': user_agent}
        try:
            reader = requests.post(url, data=params, headers=header)
        except Exception as e:
            logging.error(e)
            return ""
        msg = reader.text
        logging.info(msg)
        return msg

    def get_domains(self, type=None, offset=None, length=None):
        method = 'List'
        url = self.API_DOMAINS + method
        ret_json = self.post_data(url)
        return json.loads(ret_json, encoding='utf-8').get('domains')

    def add_domain(self, domain):
        method = 'Create'
        url = self.API_DOMAINS + method
        ret_json = self.post_data(url, param_data={'domain': domain})
        status_code = json.loads(ret_json, encoding='utf-8').get('status').get('code')
        if int(status_code) == 1:
            return "OK"
        error_code, error_message = int(status_code), self.get_error_msg(ret_json)
        logging.error("API返回错误,错误码:%d,错误说明:%s" % (error_code, error_message))
        raise DnspodApiError(error_code, error_message)

    def get_domain_id(self, domain):
        method = 'Info'
        url = self.API_DOMAINS + method
        ret_json = self.post_data(url, param_data={'domain': domain})
        if ret_json == "":
            raise DnspodApiError(-1000, "与服务器通讯通讯失败，未获取到数据")
        status_code = json.loads(ret_json, encoding='utf-8').get('status').get('code')
        if int(status_code) == 1:
            return json.loads(ret_json, encoding='utf-8').get('domain').get('id')
        error_code, error_message = int(status_code), self.get_error_msg(ret_json)
        logging.error("[__GetRecordIP:]API返回错误,错误码:%d,错误说明:%s" % (error_code, error_message))
        raise DnspodApiError(error_code, error_message)

    def get_records(self, domain):
        method = 'List'
        url = self.API_RECORDS + method
        domain_id = self.get_domain_id(domain)
        ret_json = self.post_data(url, param_data={'domain_id': domain_id})
        status_code = json.loads(ret_json, encoding='utf-8').get('status').get('code')
        if int(status_code) == 1:
            return json.loads(ret_json, encoding='utf-8').get('records')
        error_code, error_message = int(status_code), self.get_error_msg(ret_json)
        logging.error("[__GetRecordIP:]API返回错误,错误码:%d,错误说明:%s" % (error_code, error_message))
        raise DnspodApiError(error_code, error_message)

    def add_record(self, domain, sub_domain, value, record_type="A", record_line=u'默认', mx=None, ttl=600):
        method = 'Create'
        url = self.API_RECORDS + method
        domain_id = self.get_domain_id(domain)
        pam = {'domain_id': domain_id,
               'sub_domain': sub_domain,
               'record_type': record_type,
               'record_line': record_line,
               'value': value}
        if record_type == 'MX':
            if mx is None:
                pam['mx'] = mx
            else:
                pam['mx'] = 5
                logging.warning("邮件协议 MX 类型 需要添加MX优先级[1-20]")
        pam['ttl'] = ttl
        ret_json = self.post_data(url, pam)
        status_code = json.loads(ret_json, encoding='utf-8').get('status').get('code')
        if int(status_code) == 1:
            return ret_json
        error_code, error_message = int(status_code), self.get_error_msg(ret_json)
        logging.error("API返回错误,错误码:%d,错误说明:%s" % (error_code, error_message))
        raise DnspodApiError(error_code, error_message)

    def update_record(self, domain, record_id, sub_domain, value, record_type="A", record_line=u'默认', mx=None, ttl=600):
        method = 'Modify'
        url = self.API_RECORDS + method
        domain_id = self.get_domain_id(domain)
        pam = {'domain_id': domain_id,
               'record_id': record_id,
               'sub_domain': sub_domain,
               'record_type': record_type,
               'record_line': record_line,
               'value': value}
        if record_type == 'MX':
            if mx is None:
                pam['mx'] = mx
            else:
                pam['mx'] = 5
                logging.warning("邮件协议 MX 类型 需要添加MX优先级[1-20]")
        pam['ttl'] = ttl
        ret_json = self.post_data(url, pam)
        status_code = json.loads(ret_json, encoding='utf-8').get('status').get('code')
        if int(status_code) == 1:
            return ret_json
        error_code, error_message = int(status_code), self.get_error_msg(ret_json)
        logging.error("API返回错误,错误码:%d,错误说明:%s" % (error_code, error_message))
        raise DnspodApiError(error_code, error_message)

    @staticmethod
    def get_error_msg(last_json_data):
        """
        增加服务器返回错误信息
        """
        return json.loads(last_json_data, encoding='utf-8').get('status').get("message")


if __name__ == '__main__':
    from dnspod_key import KEYINFO
    initlog('./trans.log')
    dnsapi = DnspodApi(user=KEYINFO['user'], pwd=KEYINFO['pwd'])
    record_id = 353763350
    print(dnsapi.get_domains())
