# -*- coding: utf-8 -*-


import requests
import urllib.request
from bs4 import BeautifulSoup
import json
import urllib.request
import random
import time


IP_LIST = ['123.207.25.143:3128']
    # ['123.207.25.143:3128', '197.45.132.182:80',  '221.195.11.55:80']


'''利用json的信息爬取拉勾网的Python招聘信息'''


def get_json(url, page):
    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Content-Length': '25',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Cookie': ('JSESSIONID=ABAAABAACBHABBIF631C88E336CFCFA702F8D25B5928046; _ga=GA1.2.1685472951.1516888891; _'
                   'gid=GA1.2.1725380884.1516888891; _gat=1; user_trace_token=20180125220129-3dd647a8-01d8-11e8-9bec-'
                   '525400f775ce; LGSID=20180125220129-3dd64928-01d8-11e8-9bec-525400f775ce; PRE_UTM=; PRE_HOST=; '
                   'PRE_SITE=; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2F; LGUID=20180125220129-3dd64b05-01d8-11e8-9bec-'
                   '525400f775ce; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1516888891; index_location_city=%E5%85%A8%E5%'
                   '9B%BD; TG-TRACK-CODE=index_search; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1516888900; LGRID=20180'
                   '125220138-43373e48-01d8-11e8-ab9d-5254005c3644; SEARCH_ID=e0ceedcf0307444484d978595bc9f70a'),
        'Host': 'www.lagou.com',
        'Origin': 'https://www.lagou.com',
        'Referer': ('https://www.lagou.com/jobs/list_python?city=%E5%85%A8%E5%9B%BD&cl=false&fromSearch=true&label'
                    'Words=&suginput='),
        'User-Agent': ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.32'
                       '39.132 Safari/537.36'),
        'X-Anit-Forge-Code': '0',
        'X-Anit-Forge-Token': 'None',
        'X-Requested-With': 'XMLHttpRequest'
    }
    data = {
        'first': 'true',
        'pn': page,
        'kd': 'python'
    }
    return requests.post(url, data=data, headers=headers, proxies={'http': 'http://' + random.choice(IP_LIST)}).json()


def get_information(json_data, number):
    total = int(json_data['content']['positionResult']['totalCount'])

    for now_result in json_data['content']['positionResult']['result']:

        print('公司名称：' + now_result['companyFullName'] + '(' + now_result['companyShortName'] + ')')
        print('职位名称：' + now_result['positionName'])
        print('发布时间：' + now_result['createTime'])
        print('职位薪水：' + now_result['salary'])
        if now_result['district'] is not None:
            print('工作地点：' + now_result['city'] + '-' + now_result['district'])
        else:
            print('工作地点：' + now_result['city'])
        if 'education' in now_result:
            print('教育背景：' + now_result['education'])
        if 'workYear' in now_result:
            print('工作经验：' + now_result['workYear'])
        print('职位优势：' + now_result['positionAdvantage'])
        print('---------------------------------------')
        number += 1

    return number, total


def check(path):
    for c in path:
        if u'\u4e00' <= c <= u'\u9fff':
            return True
        else:
            return False


def create_ui():

    salary = ['2k以下', '2k-5k', '5k-10k', '10k-15k', '15k-25k', '25k-50k', '50k以上']

    city = input('请输入工作城市：')

    if check(city):
        city = urllib.parse.quote(city)

    is_school_job = input('是否寻求实习工作(Y/N)：')

    yx = eval(input('请选择月薪：\n1. 不限\n2. 2k以下\n3. 2k-5k\n4. 5k-10k\n5. 10k-15k\n'
                    '6. 15k-25k\n7. 25k-50k\n8. 50k以上\n请输入数字下标(1~8)：'))
    while 1:
        if type(yx) is int and 1 <= yx <= 8:
            break
        else:
            yx = eval(input('输入有误，请重新输入：'))

    url = 'https://www.lagou.com/jobs/positionAjax.json?px=default'

    if yx >= 2:
        url += '&' + 'yx=' + urllib.parse.quote(salary[yx - 2])
        pass

    url += '&' + 'city=' + city + '&needAddtionalResult=false'

    if is_school_job is 'Y':
        url += '&' + 'isSchoolJob=1'
    else:
        url += '&' + 'isSchoolJob=0'

    return url


def main():
    number = 0
    page = 1
    url = create_ui()
    number, total = get_information(get_json(url, page), number)
    page += 1
    # 默认职位数为min(6页总数，全部)
    while number <= total and page <= 6:
        number, total = get_information(get_json(url, page), number)
        page += 1
        time.sleep(6)


if __name__ == '__main__':
    main()
