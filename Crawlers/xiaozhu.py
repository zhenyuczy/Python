# -*- coding: utf-8 -*-


import requests
from bs4 import BeautifulSoup


'''爬取http://bj.xiaozhu.com的1-5页的租房信息'''


DOWNLOAD_URL = 'http://bj.xiaozhu.com'


def download_page(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/63.0.3239.132 Safari/537.36'
    }

    return requests.get(url, headers=headers).content


def parse_page(html):
    soup = BeautifulSoup(html, 'html.parser')
    # print(soup)
    title = soup.select('body > div.wrap.clearfix.con_bg > div.con_l > div.pho_info > h4 > em')[0].get_text()
    address = soup.select('body > div.wrap.clearfix.con_bg > div.con_l > div.pho_info > p')[0].get('title')
    price = soup.select('#pricePart > div.day_l > span')[0].get_text()
    picture = soup.select('#curBigImage')[0].get('src')
    landlord_name = soup.select('#floatRightBox > div.js_box.clearfix > div.w_240 > h6 > a')[0].get_text()
    landlord_pic = soup.select('#floatRightBox > div.js_box.clearfix > div.member_pic > a')[0].get('href')
    if soup.select('#floatRightBox > div.js_box.clearfix > div.w_240 > h6 > span')[0].get('class')[0] == \
            'member_girl_ico':
        landlord_sex = 'female'
    else:
        landlord_sex = 'male'

    print('房子标题：' + title)
    print('房子地址：' + address)
    print('房子价格：' + str(price))
    print('房子照片：' + picture)
    print('房东姓名：' + landlord_name + '  ' + '性别：' + landlord_sex)
    print('房东照片：' + landlord_pic)
    print('---------------------------')


def get_all_house_url_of_this_page(html):
    soup = BeautifulSoup(html, 'html.parser')
    house_list = soup.select('#page_list > ul > li')
    for i in house_list:
        parse_page(download_page(i.select('a[target="_blank"]')[0].get('href')))


def get_next_url(source):
    soup = BeautifulSoup(source, 'lxml')
    return soup.select('#page_list > div.pagination_v2.pb0_vou > a.font_st').pop().get('href')


def main():
    number = 1
    url = DOWNLOAD_URL
    while number <= 5:
        html = download_page(url)
        get_all_house_url_of_this_page(html)
        url = get_next_url(html)
        # print(url)
        number += 1


if __name__ == '__main__':
    main()
