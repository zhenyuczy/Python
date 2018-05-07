# -*- coding: utf-8 -*-


import urllib.request
import urllib.error
from selenium import webdriver
import random
import urllib.parse
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import json
import time
import requests
import os


# 注意事项：有些下载链接可能失效，要注意处理

IP_LIST = ['50.113.182.84:3128', '89.236.17.108:3128', '201.116.199.243:3128', '47.88.218.44:3128',
           '125.212.207.121:3128']
USER_AGENT = ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
              'Chrome/63.0.3239.132 Safari/537.36')


def download_image(url, path, number):
    headers = {
        'user-agent': USER_AGENT
    }
    my_path = path + '/pic' + str(number + 1) + '.jpg'

    if os.path.exists(my_path) is False:
        try:
            proxies = {'http': 'http://' + random.choice(IP_LIST)}
            response = requests.get(url, headers=headers, proxies=proxies)
            number += 1
            print('下载第{0}张图片'.format(number))
            print(url)
            open(my_path, 'wb').write(response.content)
        except:
            print('error...')

    return number


def down_page(driver, times):
    for i in range(times):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(8)


def get_chrome_options():
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    # chrome_options.add_argument('--proxy-server={0}'.format(random.choice(IP_LIST)))
    chrome_options.add_argument('--user-agent={0}'.format(USER_AGENT))
    prefs = {
        'profile.managed_default_content_settings.images': 2
    }
    chrome_options.add_experimental_option('prefs', prefs)
    return chrome_options


def get_page_source(url):
    chrome_options = get_chrome_options()
    driver = webdriver.Chrome(chrome_options=chrome_options)
    driver.get(url)

    down_page(driver, 5)

    return driver.page_source


def get_all_image_url(source, path, number):
    soup = BeautifulSoup(source, 'lxml')
    # print(soup)
    image_list = soup.find_all('div', class_="rg_meta notranslate")
    for image in image_list:

        image_url = json.loads(image.get_text())['ou']
        number = download_image(image_url, path, number)
        time.sleep(5)

    return number


def check_is_chinese(text):
    for ch in text:
        if u'\u4e00' <= ch <= u'\u9fff':
            return True
        else:
            return False


def main():

    text = input('请输入要搜索的图片内容：')
    if check_is_chinese(text):
        text = urllib.parse.quote(text)

    path = input('请输入存储图片的路径：')

    url = 'https://www.google.com/search?q=' + text + '&source=lnms&tbm=isch'

    number = 0
    number = get_all_image_url(get_page_source(url), path, number)

    print('------------------------------------------------------------\n下载结束，共下载{0}张图片'.format(number))


if __name__ == '__main__':
    main()
