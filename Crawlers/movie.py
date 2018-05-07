# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup


'''读取豆瓣Top250的电影名'''


DOWNLOAD_URL = 'http://movie.douban.com/top250'


def download_page(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    return response.content


def parse_html(html, movies):
    soup = BeautifulSoup(html, 'html.parser')

    move_list_soup = soup.find('ol', {'class': 'grid_view'})

    for each_move_li in move_list_soup.find_all('li'):
        move_information = each_move_li.find('div', {'class': 'hd'})
        move_title = move_information.find('span', {'class': 'title'}).getText()
        movies.append(move_title)

    next_page = soup.find('span', {'class': 'next'}).find('a')
    if next_page:
        return DOWNLOAD_URL + next_page['href']
    return None


def main():
    # print(download_page(DOWNLOAD_URL))
    url = DOWNLOAD_URL
    movies = []
    while url:
        url = parse_html(download_page(url), movies)

    print(len(movies))
    # f = open("", "w")
    for each_movie in movies:
        # f.writelines(each_movie + '\n')
        print(each_movie)
    # f.close()


if __name__ == '__main__':
    main()
