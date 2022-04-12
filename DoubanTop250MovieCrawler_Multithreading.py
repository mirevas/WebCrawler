##############################################################################
# Author: @mirevas
# Date: 2022.4.12
# Reference：https://blog.csdn.net/jclian91/article/details/80738749
#############################################################################

import time
import os
import requests
import random
import urllib.request
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, wait, ALL_COMPLETED

def download_picture(url):

    uapools = [
'User-Agent:Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.94 Safari/537.36',
'User-Agent:Mozilla/5.0 (iPhone; CPU iPhone OS 6_1_4 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) CriOS/27.0.1453.10 Mobile/10B350 Safari/8536.25',
'User-Agent:Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36',
'User-Agent:Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.11 (KHTML, like Gecko) Ubuntu/11.10 Chromium/27.0.1453.93 Chrome/27.0.1453.93 Safari/537.36',
'User-Agent:Mozilla/5.0 (Linux; Android 4.0.4; Galaxy Nexus Build/IMM76B) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.133 Mobile Safari/535.19',
'User-Agent:Mozilla/5.0 (Linux; Android 4.1.2; Nexus 7 Build/JZ054K) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Safari/535.19',
'User-Agent:Mozilla/5.0 (Android; Mobile; rv:14.0) Gecko/14.0 Firefox/14.0',
'User-Agent:Mozilla/5.0 (Linux; Android 4.1.2; Nexus 7 Build/JZ054K) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Safari/535.19',
'User-Agent:Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:21.0) Gecko/20100101 Firefox/21.0',
'User-Agent:Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:21.0) Gecko/20130331 Firefox/21.0',
'User-Agent:Mozilla/5.0 (Windows NT 6.2; WOW64; rv:21.0) Gecko/20100101 Firefox/21.0']

    thisua = random.choice(uapools)
    headers = {
       'User-Agent':thisua, 
        'Host': 'movie.douban.com'
    }

    r = requests.get(url,headers = headers)
    soup = BeautifulSoup(r.text, "lxml")
    content = soup.find('div', class_='article')
    images = content.find_all('img')
    picture_name_list = [image['alt'] for image in images]
    picture_link_list = [image['src'] for image in images]
    
    for picture_name, picture_link in zip(picture_name_list, picture_link_list):
        print("Downloading %s" % picture_name)
        urllib.request.urlretrieve(picture_link, './DoubanTop250Movies/%s.jpg' % picture_name)


def mkdir(path):
	folder = os.path.exists(path)
	if not folder:                   
		os.makedirs(path)            
		print("Create new directory: %s" % path)		


def main():
    file_name = "DoubanTop250Movies"
    mkdir(file_name)
    start_urls = ["https://movie.douban.com/top250"]
    for i in range(1, 10):
        start_urls.append("https://movie.douban.com/top250?start=%d&filter=" % (25 * i))

    t1 = time.time()
    executor = ThreadPoolExecutor(max_workers=10)  
    future_tasks = [executor.submit(download_picture, url) for url in start_urls]
    wait(future_tasks, return_when=ALL_COMPLETED)

    print('*' * 50)
    t2 = time.time()
    print('Multithreading downloading time：%s' % (t2 - t1))
    print('*' * 50)

main()