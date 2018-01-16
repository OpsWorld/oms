# -*- coding: utf-8 -*-
# author: itimor

import requests
# from omsBackend.settings import salt_info

restful = {
    "login": "/login",
    "jobs": "/jobs"
}
header = {"Accept": "application/json"}

salt_info = {
    "url": "https://192.168.6.99:8080",
    "username":"salt",
    "password": "123"
}

class SaltAPI(object):
    token = ''

    def __init__(self, url, username, password):
        self.__url = url
        self.__username = username
        self.__password = password
        self.__header = header

    def get_token(self):
        ''' user login and get token id '''
        data = {
            "username": self.__username,
            "password": self.__password,
            "eauth": "pam"
        }
        loginurl = self.__url + restful["login"]
        req = requests.post(loginurl, data=data, headers=self.__header, verify=False)
        try:
            self.token = req.json()["return"][0]["token"]
            print(self.token)
            return self.token
        except KeyError:
            raise KeyError

    def check_jid(self, jid):
        self.__header['X-Auth-Token'] = self.get_token()
        header = self.__header
        jid_url = self.__url + "{0}/{1}".format(restful["jobs"], jid)
        req = requests.get(jid_url, headers=header, verify=False)
        return req.json()


def main():
    sapi = SaltAPI(url=salt_info["url"], username=salt_info["username"], password=salt_info["password"])
    sapi.get_token()


if __name__ == '__main__':
    main()
