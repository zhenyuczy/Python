# -*- coding: utf-8 -*-


import requests
import urllib.request
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
import random
from selenium.webdriver.chrome.options import Options
import time


'''使用selenium&headless chrome下载煎蛋网妹子图最新的6页jpg图片'''


DOWNLOAD_URL = 'http://jandan.net/ooxx'


def get_proxy():
    ip_list = ['123.207.25.143:3128', '117.158.57.2:3128']
    proxy = urllib.request.ProxyHandler({'http': random.choice(ip_list)})
    opener = urllib.request.build_opener(proxy)
    opener.addheaders = [('User-Agent',
                          'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/63.0.3239.132 Safari/537.36')]
    urllib.request.install_opener(opener)


def query_ip():
    response = urllib.request.urlopen('http://www.whatismyip.com.tw')
    html = response.read().decode('utf-8')
    print(html)


def download_image(url, path, index):
    # response = urllib.request.urlopen(DOWNLOAD_URL)
    # return response.read()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/63.0.3239.132 Safari/537.36'
    }
    open(path + '\picture' + str(index) + '.jpg', 'wb').write(requests.get(url, headers=headers).content)
    return index + 1


def download_page(url):
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(chrome_options=chrome_options)
    driver.get(url)
    return driver.page_source


def parse_page(page_data, path, index):
    # print(page_data)
    soup = BeautifulSoup(page_data, 'lxml')
    next_url = 'http:' + soup.find('a', {'class': 'previous-comment-page'})['href']
    image_lists = soup.find('ol', {'class': 'commentlist'}).find_all('li')
    for each_list in image_lists:
        target = each_list.find('div', {'class': 'row'})
        # 跳过广告
        if target is not None:
            # 跳过被删除的图片
            if target.find('div', {'class': 'text'}).find('p', {'class': 'bad-content'}) is None:
                # <li></li> 存在多张图片的情况
                image_urls = target.find('div', {'class': 'text'}).find('p').find_all('img')
                for each_url in image_urls:
                    # 去掉gif图片
                    if '.gif' not in each_url['src']:
                        print('下载第{0}张图片......'.format(index))
                        index = download_image(each_url['src'], path, index)
                    else:
                        pass
                else:
                    pass
            else:
                pass
        else:
            pass
    else:
        pass
    return next_url, index


'''
def get_page_num(page_data):
    soup = BeautifulSoup(page_data, 'lxml')
    page_num_text = soup.find('span', {'class': 'current-comment-page'}).getText()
    a = page_num_text.find('[') + 1
    b = page_num_text.find(']')
    return int(page_num_text[a:b])


def new_web(page_num):
    return DOWNLOAD_URL + '/page-' + str(page_num) + '#comments'
'''


def main():
    path = input('请输入要存储的文件夹路径：')
    url = DOWNLOAD_URL
    number = index = 1
    while number <= 6:
        # 重新代理
        get_proxy()
        # query_ip()
        print('当前要下载的页面：' + url)
        url, index = parse_page(download_page(url), path, index)
        number += 1
        # 休息一会
        time.sleep(12)
    else:
        pass


if __name__ == '__main__':
    main()
