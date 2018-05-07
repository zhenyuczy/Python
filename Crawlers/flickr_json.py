# -*- coding: utf-8 -*-

import requests
import json
import time
import random
import urllib
import urllib.error
from selenium import webdriver
import json
import os
from bs4 import BeautifulSoup


USER_AGENT = ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
              'Chrome/63.0.3239.132 Safari/537.36')

IP_LIST = ['50.113.182.84:3128', '89.236.17.108:3128']


def download_image(url, path, image_id, stars):
    headers = {
        'user-agent': USER_AGENT
    }
    my_path = path + r'\pic' + image_id + 'stars' + stars + '.jpg'
    if os.path.exists(my_path) is False:
        try:
            response = requests.get(url, headers=headers, proxies={'http': 'http://' + random.choice(IP_LIST)})
            open(my_path, 'wb').write(response.content)
        except:
            print('Error...')

    time.sleep(2)


def get_chrome_options():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--proxy-server={0}'.format(random.choice(IP_LIST)))
    chrome_options.add_argument('--user-agent={0}'.format(USER_AGENT))
    prefs = {
        'profile.managed_default_content_settings.images': 2
    }
    chrome_options.add_experimental_option('prefs', prefs)
    return chrome_options


def get_all_image_url(url, path, number):
    # selenium 获取json
    target = None
    while target is None:
        try:
            chrome_options = get_chrome_options()
            driver = webdriver.Chrome(chrome_options=chrome_options)
            driver.get(url)
            soup = BeautifulSoup(driver.page_source, 'lxml')
            target = soup.get_text()
        except:
            print("Connection refused by the server..")
            time.sleep(5)
            print("Let me continue...")
            continue

    json_data = json.loads(target)
    '''
    # requests 获取json
    headers = {
        'user-agent': USER_AGENT
    }
    json_data = requests.get(url, headers=headers, proxies={'http': 'http://' + random.choice(IP_LIST)}).json()
    '''
    for now_image in json_data['photos']['photo']:
        stars = now_image['count_faves']
        image_id = now_image['id']
        # 也可以用farm + server + id_secret_b + .jpg
        if 'url_l_cdn' in now_image:  # 1024
            image_url = now_image['url_l_cdn']

        elif 'url_c_cdn' in now_image:  # 800
            image_url = now_image['url_c_cdn']

        elif 'url_z_cdn' in now_image:  # 640
            image_url = now_image['url_z_cdn']

        elif 'url_m_cdn' in now_image:  # 500
            image_url = now_image['url_m_cdn']

        elif 'url_n_cdn' in now_image:  # 320
            image_url = now_image['url_n_cdn']

        elif 'url_s_cdn' in now_image:  # 240
            image_url = now_image['url_s_cdn']

        elif 'url_q_cdn' in now_image:  # 150
            image_url = now_image['url_q_cdn']

        elif 'url_t_cdn' in now_image:  # 100
            image_url = now_image['url_t_cdn']

        elif 'url_sq_cdn' in now_image:  # 75
            image_url = now_image['url_sq_cdn']

        number += 1
        print('下载第{0}张图片：'.format(number))
        print(image_url)
        download_image(image_url, path, image_id, stars)

    return number


def update(per_page, page):
    if per_page == 25:
        if page == 1:
            return 25, 2
        else:
            return 50, 2

    elif per_page == 50:
        return 100, 2

    else:
        return 100, page + 1


def check_is_chinese(path):
    for c in path:
        if u'\u4e00' <= c <= u'\u9fff':
            return True
        else:
            return False


def main():

    text = input('请输入需要搜索图片的信息，输入形式为中文或者英文：')

    if check_is_chinese(text):
        text = urllib.parse.quote(text)
    path = input('请输入要存储的路径：')

    head = ('https://api.flickr.com/services/rest?sort=relevance&parse_tags=1&content_type=7&extras=can_comment%2Ccount'
            '_comments%2Ccount_faves%2Cdescription%2Cisfavorite%2Clicense%2Cmedia%2Cneeds_interstitial%2Cowner_name%2Cp'
            'ath_alias%2Crealname%2Crotation%2Curl_c%2Curl_l%2Curl_m%2Curl_n%2Curl_q%2Curl_s%2Curl_sq%2Curl_t%2Curl_z&'
            'per_page=')

    mid = '&lang=zh-Hant-HK&text=' + text + '&viewerNSID=&method=flickr.photos.search&csrf=&api_key='

    tail = '&format=json&hermes=1&hermesClient=1&reqId='

    api_key = 'd52d1fd023e957a8f85f8a2f697b6280'

    req_id = '7c1c503f'

    number = 0
    per_page = 25
    page = 1
    # 第一页json数据虽然没有监察到，但是输入链接可以获取
    while page <= 2:
        url = head + str(per_page) + '&page=' + str(page) + mid + api_key + tail + req_id + '&nojsoncallback=1'
        number = get_all_image_url(url, path, number)
        per_page, page = update(per_page, page)
        time.sleep(6)

    print('---------------------------------------------------------\n下载结束，共下载{0}张图片'.format(number))


if __name__ == '__main__':
    main()