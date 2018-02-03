# -*- coding: utf-8 -*-
# author: itimor

import requests
import datetime

salt_info = {
    "url": "http://salt.tbsysmanager.com:8080",
    "username": "saltdev",
    "password": "FF01VeF4hs1FqZ5M"
}


class SaltAPI(object):
    def __init__(self, url, username, password):
        self.__url = url
        self.__username = username
        self.__password = password
        self.__header = dict()
        self.__header["Accept"] = "application/json"
        self.token_s_time = ''
        self.__token = self.get_token()

    def get_token(self, prefix='/login'):
        """
        登录获取token
        """

        data = {
            "username": self.__username,
            "password": self.__password,
            "eauth": "pam"
        }
        loginurl = self.__url + prefix
        req = requests.post(loginurl, data=data, headers=self.__header, verify=False)
        try:
            token = req.json()["return"][0]["token"]
            self.token_s_time = datetime.datetime.now()
            return token
        except KeyError:
            raise KeyError

    def salt_request(self, data, prefix='/'):
        """
        接收请求，返回结果
        """

        token_e_time = datetime.datetime.now()
        print("token_e_time: %s" % token_e_time)
        print("token_s_time: %s" % self.token_s_time)

        if (token_e_time - self.token_s_time).seconds / 3600 > 3:
            print("salt-api token is Expired")
            self.get_token()

        url = self.__url + prefix
        self.__header["X-Auth-Token"] = self.__token

        # 传入data参数字典，data为None 则方法为get，有date为post方法
        if data:
            req = requests.post(url, data=data, headers=self.__header, verify=False)
        else:
            req = requests.get(url, headers=self.__header)

        return req.json()

    def list_key(self):
        """
        获取包括认证、未认证salt主机
        """

        prefix = '/keys'
        content = self.salt_request(None, prefix)

        accepted = content['return']['minions']
        denied = content['return']['minions_denied']
        unaccept = content['return']['minions_pre']
        rejected = content['return']['minions_rejected']
        return {"accepted": accepted, "denied": denied, "unaccept": unaccept, "rejected": rejected}

    def accept_key(self, key_id):
        """
        接受salt主机
        """

        data = {'client': 'wheel', 'fun': 'key.accept', 'match': key_id}
        content = self.salt_request(data)
        ret = content['return'][0]['data']['success']
        return ret

    def delete_key(self, key_id):
        """
        删除salt主机
        """

        data = {'client': 'wheel', 'fun': 'key.delete', 'match': key_id}
        content = self.salt_request(data)
        ret = content['return'][0]['data']['success']
        return ret

    def minions_status(self):
        """
        salt主机存活检测
        """

        data = {'client': 'runner', 'fun': 'manage.status'}
        content = self.salt_request(data)
        ret = content['return'][0]
        return ret

    def remote_cmd(self, tgt, fun, client='local_async', expr_form='list', arg='', **kwargs):
        """
        异步执行远程命令、部署模块
        """

        data = {'client': client, 'tgt': tgt, 'fun': 'cmd.run', 'arg': arg, 'expr_form': expr_form}
        content = self.salt_request(data)
        ret = content['return'][0]['jid']
        print(content)
        return ret

    def get_result(self, jid):
        """
        通过jid获取执行结果
        """

        data = {'client': 'runner', 'fun': 'jobs.lookup_jid', 'jid': jid}
        content = self.salt_request(data)
        ret = content['return'][0]
        return ret

    def get_job_info(self, jid=''):
        """
        获取任务的详细执行信息
        """

        if jid:
            prefix = '/jobs/' + jid
        else:
            prefix = '/jobs'

        content = self.salt_request(None, prefix)
        ret = content['return'][0]
        return ret

    def running_jobs(self):
        """
        获取运行中的任务
        """

        data = {'client': 'runner', 'fun': 'jobs.active'}
        content = self.salt_request(data)
        ret = content['return'][0]
        return ret

    def check_job(self, jid):
        """
        检查任务是否已经执行并成功退出
        """

        data = {'client': 'runner', 'fun': 'jobs.exit_success', 'jid': jid}
        content = self.salt_request(data)
        ret = content['return'][0]
        return ret

    def sync_remote_server(self, tgt=[], arg=[], expr_form='list'):
        """
        获取远程主机信息
        """

        data = {'client': 'local', 'tgt': tgt, 'fun': 'grains.item', 'arg': arg, 'expr_form': expr_form}
        content = self.salt_request(data)['return']
        return content


def main():
    sapi = SaltAPI(url=salt_info["url"], username=salt_info["username"], password=salt_info["password"])
    # cmd = 'netstat'
    tgt = sapi.minions_status()['up']
    arg = ['osfinger', 'ipv4', 'cpu_model', 'num_cpus', 'memory_info', 'disk_info']
    # jid = sapi.remote_cmd(tgt=tgt, fun='cmd.run', arg=cmd)
    # print(jid)
    #print(sapi.sync_remote_server(tgt, arg))
    print(sapi.minions_status())


if __name__ == '__main__':
    main()
