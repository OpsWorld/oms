# -*- coding: utf-8 -*-
# author: itimor

from __future__ import unicode_literals
import sys
import requests
import logging


def initlog(logfile, logname):
    """
    创建日志实例
    """
    # logger = logging.getLogger(logname) # 有logname就不生产日志
    logger = logging.getLogger()
    hdlr = logging.FileHandler(logfile)
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr)
    logger.setLevel(logging.NOTSET)
    return logger


class GodaddyApiError(Exception):
    def __init__(self, error_message, *args, **kwargs):
        super(GodaddyApiError, *args, **kwargs)
        self.error_message = error_message


class GodaddyApi(object):
    def __init__(self, api_key, api_secret, delegate=None, log_level=None):

        # Logging setup
        self._api_key = api_key
        self._api_secret = api_secret
        self._delegate = delegate

        # Templates
        self._SSO_KEY_TEMPLATE = 'sso-key {api_key}:{api_secret}'
        self.API_TEMPLATE = 'https://api.godaddy.com/v1'
        self.DOMAINS = '/domains'
        self.DOMAIN_INFO = '/domains/{domain}'
        self.RECORDS = '/domains/{domain}/records'
        self.RECORDS_TYPE = '/domains/{domain}/records/{type}'
        self.RECORDS_TYPE_NAME = '/domains/{domain}/records/{type}/{name}'

    def get_headers(self):
        headers = {
            'Authorization': self._SSO_KEY_TEMPLATE.format(api_key=self._api_key,
                                                           api_secret=self._api_secret)
        }

        if self._delegate is not None:
            headers['X-Shopper-Id'] = self._delegate

        return headers

    def _build_record_url(self, domain, record_type=None, name=None):
        url = self.API_TEMPLATE

        if name is None and record_type is None:
            url += self.RECORDS.format(domain=domain)
        elif name is None and record_type is not None:
            url += self.RECORDS_TYPE.format(domain=domain, type=record_type)
        elif name is not None and record_type is None:
            raise ValueError("If name is specified, type must also be specified")
        else:
            url += self.RECORDS_TYPE_NAME.format(domain=domain, type=record_type, name=name)

        return url

    def _get_json_from_response(self, url, json=None, **kwargs):
        return self._request_submit(requests.get, url=url, json=json, **kwargs).json()

    def _log_response_from_method(self, req_type, resp):
        logging.debug('[{req_type}] response: {resp}'.format(resp=resp, req_type=req_type.upper()))
        logging.debug('Response data: {}'.format(resp.content))

    def _patch(self, url, json=None, **kwargs):
        return self._request_submit(requests.patch, url=url, json=json, **kwargs)

    def _put(self, url, json=None, **kwargs):
        return self._request_submit(requests.put, url=url, json=json, **kwargs)

    @staticmethod
    def _remove_key_from_dict(dictionary, key_to_remove):
        return dict((key, value) for key, value in dictionary.items() if key != key_to_remove)

    def _request_submit(self, func, **kwargs):
        resp = func(headers=self.get_headers(), **kwargs)
        self._log_response_from_method(func.__name__, resp)
        self._validate_response_success(resp)
        return resp

    def _scope_control_account(self, account):
        if account is None:
            return self.account
        else:
            return account

    @staticmethod
    def _validate_response_success(response):
        try:
            response.raise_for_status()
        except Exception as e:
            raise GodaddyApiError(response.json())

    def get_domain_info(self, domain):
        url = self.API_TEMPLATE + self.DOMAIN_INFO.format(domain=domain)
        return self._get_json_from_response(url)

    def get_domains(self):
        url = self.API_TEMPLATE + self.DOMAINS
        data = self._get_json_from_response(url)
        return data

    def update_domain(self, domain, **kwargs):
        update = {}
        for k, v in kwargs.items():
            update[k] = v
        url = self.API_TEMPLATE + self.DOMAIN_INFO.format(domain=domain)
        self._patch(url, json=update)
        logging.info("Updated domain {} with {}".format(domain, update))

    def get_records(self, domain, record_type=None, name=None):
        url = self._build_record_url(domain, record_type=record_type, name=name)
        data = self._get_json_from_response(url)
        logging.debug('Retrieved {} record(s) from {}.'.format(len(data), domain))
        return data

    def add_record(self, domain, sub_domain, value, record_type="A", ttl=600):
        record = {
            'type': record_type,
            'name': sub_domain,
            'data': value,
            'ttl': ttl
        }
        self.add_records(domain, [record])
        return True

    def add_records(self, domain, records):
        """
        添加记录用的patch, 没有post, 好傻逼的api
        """
        url = self.API_TEMPLATE + self.RECORDS.format(domain=domain)
        self._patch(url, json=records)
        logging.debug('Added records @ {}'.format(records))
        return True

    def replace_records(self, domain, records, record_type=None, name=None):
        url = self._build_record_url(domain, name=name, record_type=record_type)
        self._put(url, json=records)
        return True

    def update_ip(self, ip, record_type='A', domains=None, subdomains=None):
        if domains is None:
            domains = self.get_domains()
        elif sys.version_info < (3, 0):
            if type(domains) == str:
                domains = [domains]
        elif sys.version_info >= (3, 0) and type(domains) == str:
            domains = [domains]
        elif type(domains) == list:
            pass
        else:
            raise SystemError("Domains must be type 'list' or type 'str'")
        for domain in domains:
            a_records = self.get_records(domain, record_type=record_type)
            for record in a_records:
                r_name = record['name']
                r_ip = record['data']
                if not r_ip == ip:
                    if ((subdomains is None) or
                            (type(subdomains) == list and subdomains.count(r_name)) or
                            (type(subdomains) == str and subdomains == r_name)):
                        record.update(data=ip)
                        self.update_record(domain, record)
        return True

    def delete_record(self, domain, name, record_type):
        records = self.get_records(domain)
        if records is None:
            return False
        save = list()
        deleted = 0
        for record in records:
            if record_type == record['type'] and name == record['name']:
                deleted += 1
            else:
                save.append(record)
        self.replace_records(domain, records=save)
        logging.info("Deleted {} records @ {}".format(deleted, domain))
        return True

    def update_record(self, domain, name, value, record_type='A', ttl=600):
        """
        修改只能修改 value和ttl, 好傻逼的api
        """
        record = {
            'type': record_type,
            'name': "ddd",
            'data': value,
            'ttl': ttl
        }
        url = self.API_TEMPLATE + self.RECORDS_TYPE_NAME.format(domain=domain, type=record_type, name=name)
        self._put(url, json=record)
        logging.info('Updated record. Domain {} name {} type {}'.format(domain, name, record_type))
        return True


if __name__ == '__main__':
    from dnsapi_key import GODADDY_KEYINFO

    initlog('./dnsapi.log', 'GoDaddyApi')

    godaddy = GodaddyApi(GODADDY_KEYINFO['key'], GODADDY_KEYINFO['secret'])
    record = {
        'type': 'A',
        'name': 'aaa',
        'data': '1.1.1.3',
        'ttl': 3600
    }
    records = [{'data': '1.1.1.123', 'name': 'blog', 'ttl': 3600, 'type': 'A'},
               {'type': 'A', 'name': 'ggg', 'data': '1.1.1.2', 'ttl': 600}
               ]
    print(godaddy.get_domains())
