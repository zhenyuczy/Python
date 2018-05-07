# -*- coding: utf-8 -*-

import requests
import urllib.request
import hashlib
import time
import json
import random

'''模拟有道翻译，需要获取盐值计算方法'''


def user_input():
    return input('请输入要翻译的内容：')


def translate():

    url = 'http://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule'

    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/63.0.3239.132 Safari/537.36'
    }
    data = {}
    # data['i'] = '好'
    data['i'] = user_input()
    data['from'] = 'AUTO'
    data['to'] = 'AUTO'
    data['smartresult'] = 'dict'
    data['client'] = 'fanyideskweb'
    data['doctype'] = 'json'
    data['version'] = '2.1'
    data['keyfrom'] = 'fanyi.web'
    data['action'] = 'FY_BY_CLICKBUTTION'
    data['typoResult'] = 'false'
    salt_value = str(int(time.time() * 1000) + random.randint(0, 9))
    sign_value = hashlib.md5((data['client'] + data['i'] + salt_value + r'aNPG!!u6sesA>hBAW1@(-').encode(
        'utf-8')).hexdigest()

    data['salt'] = salt_value
    data['sign'] = sign_value

    data = urllib.parse.urlencode(data).encode('utf-8')

    req = urllib.request.Request(url, data, header)
    # req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)
    # Chrome/63.0.3239.132 Safari/537.36')

    response = urllib.request.urlopen(req)

    html = response.read().decode('utf-8')
    target = json.loads(html)
    # print(target['translateResult'][0][0]['src'])
    print('翻译为：' + target['translateResult'][0][0]['tgt'])


def main():
    translate()


if __name__ == '__main__':
    main()
