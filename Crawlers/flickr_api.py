# -*- coding: utf-8 -*-
import flickrapi
import time
import random


# 请输入flickr api and secret，前面的u不要去掉

api_key = u''
api_secret = u''

flickr = flickrapi.FlickrAPI(api_key, api_secret, cache=True)

# -01-30
# -07-29

# -07-30
# -01-29


def download(y, m, min_time, max_time):
    print(min_time, max_time)
    try:
        photos = flickr.walk(tags='bijou', extras='url_sq',
                             min_upload_date=min_time,
                             max_upload_date=max_time)
    except Exception as e:
        print('Error')

    f = open('D:/tags=bijou/url' + str(y) + '0' + str(m) + '.txt', 'w+')
    number = 0
    for photo in photos:
        url = photo.get('url_sq')
        f.writelines(str(url) + '\n')
        number += 1
    f.close()
    # print('%d年%d月' % (y, m))
    print(number)
    time.sleep(random.randint(12, 16))


for i in range(2004, 2018):
    min_time = str(i) + '-01-30'
    max_time = str(i) + '-07-29'
    download(i, 1, min_time, max_time)

    min_time = str(i) + '-07-30'
    max_time = str(i + 1) + '-01-29'
    download(i, 7, min_time, max_time)