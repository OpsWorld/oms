# -*- coding: utf-8 -*-
# author: itimor

from __future__ import unicode_literals
import requests
import json
import logging
from dnspod_key import KEYINFO


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
            pam = [('login_email', self.Duser),
                   ('login_password', self.Dpwd),
                   ('format', self.Dformat),
                   ('lang', self.Dlang),
                   ('error_on_empty', self.Derror_on_empty)]
        else:
            pam = [('login_token', self.Dtoken),
                   ('format', self.Dformat),
                   ('lang', self.Dlang),
                   ('error_on_empty', self.Derror_on_empty)]
        if self.Duser_id is not None:
            pam.append(('user_id', self.Duser_id))
        return pam

    def post_data(self, url, param_data=None):
        # type:([str,dict]) -> str
        """
        将 方法,基础url,参数合并成 url请求,并向服务器发送获取结果然后返回
        """
        user_agent = "1234567654321"
        auth_param = self.auth_param()
        if param_data:
            params = dict(auth_param + param_data)
        else:
            params = dict(auth_param)
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
        """参见http://www.dnspod.cn/docs/domains.html#id2"""
        method = 'List'
        url = self.API_DOMAINS + method
        ret_json = self.post_data(url)
        return json.loads(ret_json, encoding='utf-8').get('domains')

    def add_domain(self):
        """参见http://www.dnspod.cn/docs/domains.html#id2"""
        url = "https://dnsapi.cn/Domain.Create"
        # TODO
        raise NotImplementedError()

    def add_record(self, sub_domain, domain, rec_value, record_type="A", record_line="默认".encode('utf-8'), mx=None,
                   ttl=600):
        url = "https://dnsapi.cn/Record.Create"
        domain_id = self.__get_domain_id(domain)
        pam = [('domain_id', domain_id),
               ('sub_domain', sub_domain),
               ('record_type', record_type),
               ('record_line', record_line),
               ('value', rec_value)]
        if record_type == 'MX':
            if mx is None:
                pam.append(('mx', mx))
            else:
                pam.append(('mx', '5'))
                logging.warn("邮件协议 MX 类型 需要添加MX优先级[1-20]")
        pam.append(('ttl', ttl))
        ret_json = self.post_data((url, pam))
        status_code = json.loads(ret_json, encoding='utf-8').get('status').get('code')
        if int(status_code) == 1:
            return "OK"
        error_code, error_message = int(status_code), self.get_error_msg(ret_json)
        logging.error("API返回错误,错误码:%d,错误说明:%s" % (error_code, error_message))
        raise DnspodApiError(error_code, error_message)

    def get_record_ip(self, domain, sub_domain):
        domain_id = self.__get_domain_id(domain)
        record_address = self.__get_record_ip(domain_id, sub_domain)
        logging.info("DnsPod获取到记录IP是:[%s]" % record_address)
        return record_address

    def __get_domain_id(self, domain_name):
        """http://www.dnspod.cn/docs/domains.html#id6"""
        url = "https://dnsapi.cn/Domain.Info"
        pam = [('domain', domain_name)]
        ret_json = self.post_data((url, pam))
        if ret_json == "":
            raise DnspodApiError(-1000, "与服务器通讯通讯失败，未获取到数据")
        status_code = json.loads(ret_json, encoding='utf-8').get('status').get('code')
        if int(status_code) == 1:
            return json.loads(ret_json, encoding='utf-8').get('domain').get('id')
        error_code, error_message = int(status_code), self.get_error_msg(ret_json)
        logging.error("[__GetRecordIP:]API返回错误,错误码:%d,错误说明:%s" % (error_code, error_message))
        raise DnspodApiError(error_code, error_message)

    def __get_record_id(self, domain_id, sub_domain):
        """http://www.dnspod.cn/docs/records.html#id3"""
        url = "https://dnsapi.cn/Record.List"
        if domain_id is None:
            logging.warn("参数Domain 是None 类型")
            return None
        pam = [('domain_id', domain_id), ('sub_domain', sub_domain)]
        ret_json = self.post_data((url, pam))
        status_code = json.loads(ret_json, encoding='utf-8').get('status').get('code')
        if int(status_code) == 1:
            return json.loads(ret_json, encoding='utf-8').get('records')[0].get('id')
        error_code, error_message = int(status_code), self.get_error_msg(ret_json)
        logging.error("[__GetRecordIP:]API返回错误,错误码:%d,错误说明:%s" % (error_code, error_message))
        raise DnspodApiError(error_code, error_message)

    def __get_record_ip(self, domain_id, sub_domain):
        """http://www.dnspod.cn/docs/records.html#id3"""
        url = "https://dnsapi.cn/Record.List"
        if domain_id is None:
            logging.warning("参数Domain 是None 类型")
            return None
        pam = [('domain_id', domain_id), ('sub_domain', sub_domain)]
        ret_json = self.post_data((url, pam))
        status_code = json.loads(ret_json, encoding='utf-8').get('status').get('code')
        if int(status_code) == 1:
            return json.loads(ret_json, encoding='utf-8').get('records')[0].get('value')
        error_code, error_message = int(status_code), self.get_error_msg(ret_json)
        logging.error("[__GetRecordIP:]API返回错误,错误码:%d,错误说明:%s" % (error_code, error_message))
        raise DnspodApiError(error_code, error_message)

    @staticmethod
    def get_error_info(error_code):
        if int(error_code) == -1:
            return "登陆失败"
        elif int(error_code) == -2:
            return "API使用超出限制"
        elif int(error_code) == -3:
            return "不是合法代理 (仅用于代理接口)"
        elif int(error_code) == -4:
            return "不在代理名下 (仅用于代理接口)"
        elif int(error_code) == -7:
            return "无权使用此接口"
        elif int(error_code) == -8:
            return "登录失败次数过多，帐号被暂时封禁"
        elif int(error_code) == -99:
            return "此功能暂停开放，请稍候重试"
        elif int(error_code) == 1:
            return "操作成功"
        elif int(error_code) == 2:
            return "只允许POST方法"
        elif int(error_code) == 3:
            return "未知错误"
        elif int(error_code) == 6:
            return "用户ID错误 (仅用于代理接口)"
        elif int(error_code) == 7:
            return "用户不在您名下 (仅用于代理接口)"
        else:
            return "无说明" + error_code

    @staticmethod
    def get_error_msg(last_json_data):
        """
        增加服务器返回错误信息
        """
        return json.loads(last_json_data, encoding='utf-8').get('status').get("message")


if __name__ == '__main__':
    initlog('./trans.log')
    dnsapi = DnspodApi(user=KEYINFO['user'], pwd=KEYINFO['pwd'])
    print(dnsapi.get_domains())
