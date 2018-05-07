# -*- coding: utf-8 -*-


import requests
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
import time
import random
import urllib
import os


'''爬取flickr官网搜索的图片，按照标签进行查找，下载图片并按照图片的id和星级来命名'''

DOWNLOAD_URL = 'https://www.flickr.com/search/?text='
IP_LIST = ['50.113.182.84:3128', '89.236.17.108:3128']
USER_AGENT = ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
              'Chrome/63.0.3239.132 Safari/537.36')


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


def download_image(path, url, image_id, stars):
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


def get_image_download_url(url):
    print(url)

    target = None
    while target is None:
        try:
            chrome_options = get_chrome_options()
            driver = webdriver.Chrome(chrome_options=chrome_options)
            driver.get(url)
            soup = BeautifulSoup(driver.page_source, 'lxml')
            target = soup.find('img', class_="main-photo")['src']
        except:
            print("Connection refused by the server..")
            time.sleep(5)
            print("Let me continue...")
            continue

    return 'https:' + target


def down_page(driver, times):
    for i in range(times):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(6)


def download_page(url):
    chrome_options = get_chrome_options()
    driver = webdriver.Chrome(chrome_options=chrome_options)
    driver.get(url)
    # 最初下滑4次 停止，需要点击 加载更多
    # 之后点击加载，默认下滑一次
    # 之后下滑5次 停止，需要点击 加载更多
    # 全部按5次处理
    down_page(driver, 5)
    # 等待加载
    time.sleep(6)

    return driver.page_source


def get_all_image_url(source, path, number, limit):
    soup = BeautifulSoup(source, 'lxml')
    # print(soup)
    # 跳过按钮
    next_button = None
    for image in soup.find('div', class_="view photo-list-view requiredToShowOnServer").children:

        if next_button is not None and number >= limit:
            break

        target_url = image.find('a', class_="overlay")
        if number < limit and target_url is not None:
            image_url = 'https://www.flickr.com' + target_url['href']
            # 第一个span就是星级
            stars = image.find('span', class_="icon-count").get_text()
            t = image_url.rfind('/')
            s = image_url.rfind('/', 0, t - 1) + 1
            image_id = image_url[s:t]
            number += 1
            print('下载第{0}张图片'.format(number))
            download_image(path, get_image_download_url(image_url), image_id, stars)
        elif target_url is None:
            next_button = image
            break
    '''
    image_lists = soup.find('div', class_="view photo-list-view requiredToShowOnServer").find_all('div', class_="view photo-list-photo-view")
    for image_list in image_lists:
        # 有些没有得到background_image，无法直接得到下载地址
        image_url = 'https://www.flickr.com' + image_list.find('a', class_="overlay")['href']
        number += 1
        print(image_url)
    '''
    return number, next_button


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

    next_button = ''  # 加载更多图片按钮
    number = 0        # 下载图片数目
    # 测试下载50张图片
    limit = 5
    number, next_button = get_all_image_url(download_page(DOWNLOAD_URL + text), path, number, limit)


if __name__ == '__main__':
    main()


