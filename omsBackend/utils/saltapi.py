# -*- coding: utf-8 -*-
# author: itimor

import requests

# from omsBackend.settings import salt_info

restful = {
    "login": "/login",
    "jobs": "/jobs"
}

salt_info = {
    "url": "http://192.168.6.99:8080",
    "username": "salt",
    "password": "123"
}


class SaltAPI(object):
    def __init__(self, url, username, password):
        self.__url = url
        self.__username = username
        self.__password = password
        self.__header = {}
        self.__header["Accept"] = "application/json"
        self.__token = self.get_token()

    def get_token(self):
        ''' user login and get token'''
        data = {
            "username": self.__username,
            "password": self.__password,
            "eauth": "pam"
        }
        loginurl = self.__url + restful["login"]
        req = requests.post(loginurl, data=data, headers=self.__header)
        try:
            token = req.json()["return"][0]["token"]
            return token
        except KeyError:
            raise KeyError

    def post_request(self, data, prefix='/'):
        url = self.__url + prefix
        self.__header["X-Auth-Token"] = self.__token

        # 传入data参数字典，data为None 则方法为get，有date为post方法
        if data:
            req = requests.post(url, data=data, headers=self.__header)
        else:
            req = requests.get(url, headers=self.__header)

        return req.json()

    def check_jid(self, jid):
        self.__header['X-Auth-Token'] = self.__token
        prefix = "{0}/{1}".format(restful["jobs"], jid)
        content = self.post_request(None, prefix)
        return content

    def list_key(self):
        prefix = '/keys'
        content = self.post_request(None, prefix)
        accepted = content['return']['minions']
        denied = content['return']['minions_denied']
        unaccept = content['return']['minions_pre']
        rejected = content['return']['minions_rejected']
        return {"accepted": accepted, "denied": denied, "unaccept": unaccept, "rejected": rejected}

    def accept_key(self, key_id):
        data = {'client': 'wheel', 'fun': 'key.accept', 'match': key_id}
        content = self.post_request(data)
        ret = content['return'][0]['data']['success']
        return ret

    def delete_key(self, key_id):
        data = {'client': 'wheel', 'fun': 'key.delete', 'match': key_id}
        content = self.post_request(data)
        ret = content['return'][0]['data']['success']
        return ret


def main():
    sapi = SaltAPI(url=salt_info["url"], username=salt_info["username"], password=salt_info["password"])
    print(sapi.list_key())


if __name__ == '__main__':
    main()
