# -*- coding: utf-8 -*-

import urllib.request
import random
import requests
from selenium.webdriver.chrome.options import Options
from selenium import webdriver


'''代理服务器'''

ip_list = ['120.79.133.212:8088']


# ['123.207.25.143:3128', '54.187.185.232:3128', '117.158.57.2:3128']
# 139.59.224.185:3128', '50.113.182.84:3128', '50.113.182.83:3128', '113.207.44.70:3128', '50.76.15.2:3128'
# 47.88.218.44:3128

USER_AGENT = ('Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
              'Chrome/63.0.3239.132 Safari/537.36')


def query_id():
    url = 'http://icanhazip.com'
    response = urllib.request.urlopen(url)
    print(response.read().decode('utf-8'))


def use_urllib_request():
    proxy = urllib.request.ProxyHandler({'http': random.choice(ip_list)})
    opener = urllib.request.build_opener(proxy)
    opener.addheaders = [('User-Agent', USER_AGENT)]
    urllib.request.install_opener(opener)
    query_id()


def use_requests():
    html = requests.get('http://icanhazip.com', proxies={'http': 'http://' + random.choice(ip_list)}).text
    print(html)


def use_selenium():
    # proxy = random.choice(ip_list)
    apiUrl = "http://dynamic.goubanjia.com/dynamic/get/ff91539ec23db609dc980c0545464e67.html"
    proxy = urllib.request.urlopen(apiUrl).read().decode('utf-8')

    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--proxy-server={0}'.format(proxy))
    chrome_options.add_argument('--user-agent={0}'.format(USER_AGENT))
    driver = webdriver.Chrome(chrome_options=chrome_options)
    driver.get('http://icanhazip.com')
    print(driver.page_source)


def main():
    # 使用urllib.request代理
    # use_urllib_request()

    # 使用requests代理
    # use_requests()

    # 使用selenium代理
    use_selenium()


if __name__ == '__main__':
    main()