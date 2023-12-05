# Insert your code here. 
# coding=utf-8
import json

import requests

'''
封装server酱推送

    author:anysoft@yeah.net
    date:2023-06-25 23:29:15
'''


class ServerChan(object):

    def __init__(self, secret_key):
        if not secret_key:
            raise Exception('secret_key is empty!')
        self.serverchan_url = 'https://sctapi.ftqq.com'
        self.sercret_key = secret_key
        self.headers = {
            'Content-Type': 'application/json;charset=utf-8'
        }
        self.version = 2

        if str(secret_key).startswith('SCU'):
            self.version = 1
            self.serverchan_url = 'https://sc.ftqq.com'
            self.headers = {}

        self.push_url = '{}/{}.send'.format(self.serverchan_url, secret_key)

    def query(self, pushid='', readkey=""):
        params = {
            'id': pushid,
            'readkey': readkey
        }
        return requests.get('{}/push'.format(self.serverchan_url), params=params, headers=self.headers)

    def push(self, title='', desp='', short='', channel=''):
        payload = {
            "text": title.replace(' ', '  '),
            "desp": desp
        }
        if short:
            payload.__setitem__('short', short)

        if channel:
            payload.__setitem__('channel', channel)
        data = json.dumps(payload)
        if self.version == 1:
            data = payload
        response = requests.post(self.push_url, data=data, headers=self.headers)
        if response.text.__contains__('use keys on sct.ftqq.com'):
            raise RuntimeError('use keys on sct.ftqq.com')
        return response


if __name__ == '__main__':
    pass
    # secret = ''
    # serverchan = ServerChan(secret)
    #
    # response = serverchan.push("test", 'just for test')
    # print(response.text)
    # print(response.status_code)@&m!4BaSTgM!5EVxB^o5
    # print(response.headers)
