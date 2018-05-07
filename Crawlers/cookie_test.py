# -*- coding: utf-8 -*-

import urllib
import http.cookiejar
import urllib.request
import urllib.parse
from bs4 import BeautifulSoup


'''模拟登录PAT，查询用户姓名和生日'''

filename = 'D:/cookie.txt'

user_name = input('请输入你的用户名：')
password = input('请输入你的密码：')


cookie = http.cookiejar.MozillaCookieJar(filename)

opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cookie))

post_data = urllib.parse.urlencode({'user[handle]': user_name,
                                    'user[password]': password}).encode('utf-8')

login_url = 'https://www.patest.cn/users/sign_in'

result = opener.open(login_url, post_data)

cookie.save(ignore_discard=True, ignore_expires=True)

setting_url = 'https://www.patest.cn/users/edit'

result = opener.open(setting_url)

soup = BeautifulSoup(result.read(), 'lxml')

my_name = soup.find('input', {'id': 'user_real_name'})['value']
my_birth_year = soup.find('select', {'id': 'user_birthday_1i'}).find('option', {'selected': 'selected'}).get_text()
my_birth_month = soup.find('select', {'id': 'user_birthday_2i'}).find('option', {'selected': 'selected'}).get_text()
my_birth_day = soup.find('select', {'id': 'user_birthday_3i'}).find('option', {'selected': 'selected'}).get_text()


print('用户姓名：' + my_name)
print('用户生日：' + my_birth_year + '年' + my_birth_month + my_birth_day + '日')

