# -*- coding: utf-8 -*-

import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time


'''
爬取58同城北京回收市场前3页物品的信息，找到并进入每一个物品的各自链接，
在新链接中获取物品信息，并尝试获得js生成的浏览次数信息。
筛选浏览次数 >= 6666（或者价格 >= 666）、服务区域中包含海淀、朝阳的物品。
注意事项：
1，去掉重复贴子
2, 对于没有区域的贴子，则放弃
3，对于没有浏览次数的贴子，寻找价格，对于没有价格的贴子，则放弃
'''

DOWNLOAD_URL = 'http://bj.58.com/huishou'


def download_page(url):
    options = Options()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    return driver.page_source


def check_address_is_exist(soup):
    if soup.find('div', {'class': 'su_con quyuline'}) is None:
        return False
    else:
        return True


def check_views_is_exist(soup):
    if soup.find('li', {'title': '浏览次数'}) is None:
        return False
    else:
        return True


def check_price_is_exist(soup):
    if soup.find('span', {'class': 'pri_big'}) is None:
        return False
    else:
        return True


def output_information(views, price):
    if views == '':
        return 'price: ' + price
    else:
        return 'views: ' + views


def parser_page(source, title_set):
    soup = BeautifulSoup(source, 'lxml')

    views = price = ''
    if check_views_is_exist(soup):
        views = soup.find('li', {'title': '浏览次数'}).find('em').get_text()
        if int(views) < 6666:
            return title_set
    elif check_price_is_exist(soup):  # 浏览次数不存在寻找价格
        price = soup.find('span', {'class': 'pri_big'}).get_text()
        if int(price) < 666:
            return title_set
    else:  # 放弃
        return title_set

    if check_address_is_exist(soup):
        address = soup.find('div', {'class': "su_con quyuline"}).get_text(' ', strip=True)
        address = str(address).split(' ')
        if '朝阳' not in address or '海淀' not in address:
            return title_set
    else:  # 放弃
        return title_set

    title = soup.select('#basicinfo > div.mainTitle > h1')[0].get_text().strip()
    sort = soup.select('body > div.nav > a.crb_a_2')[0].get_text().strip()

    # 精贴 和 置顶贴 多次出现
    if title not in title_set:
        print('sort: ' + sort, 'title: ' + title, 'address: ' + str(address)[1:-1],
              output_information(views, price), sep='\n')
        print('------------------------')
        title_set.add(title)

    time.sleep(3)
    return title_set


def get_all_page_url(source, answer):
    soup = BeautifulSoup(source, 'lxml')
    next_url = soup.find('a', {'class': 'next'})['href']
    table_list = soup.find_all('table')
    for table in table_list:
        # 去掉空列
        null_list = table.find_all('tr', {'class': 'ac_item none'})

        for null_item in null_list:
            null_item.decompose()
        else:
            pass

        good_list = table.find_all('tr', {'class': 'ac_item'})
        for good in good_list:
            second_td = good.select('td:nth-of-type(2)')[0]
            if second_td.find('div', {'class': 'tdiv'}) is not None:
                print(second_td.select('div.tdiv > a')[0].get('href'))
                answer = parser_page(download_page(second_td.select('div.tdiv > a')[0].get('href')), answer)
            else:
                print(second_td.find('a')['href'])
                answer = parser_page(download_page(second_td.find('a')['href']), answer)

        else:
            pass
    else:
        pass
    return next_url, answer


def main():

    url = DOWNLOAD_URL
    number = 1
    title_set = set()
    while number <= 1:
        url, title_set = get_all_page_url(download_page(url), title_set)
        number += 1
    else:
        pass


if __name__ == '__main__':
    main()
