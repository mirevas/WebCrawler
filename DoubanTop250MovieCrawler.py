##############################################################################
# Author: @mirevas
# Date: 2019.12.16
# Reference：https://blog.csdn.net/weixin_44547562/article/details/103533502
#############################################################################

import time
import requests
from bs4 import BeautifulSoup


def get_page(url, params=None, headers=None):
    response = requests.get(url, headers=headers, params=params)
    page = BeautifulSoup(response.text, 'lxml')
    print(response.url)
    print("response status code", response.status_code)
    
    return page

def download():
    title_list = []  
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.83 Safari/537.36Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.83 Safari/537.36Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
        'Host': 'movie.douban.com'
    }

    for i in range(11):
        params = {"start": (i * 25)}
        print("Downloading page",i,"...")
        page = get_page('https://movie.douban.com/top250', params=params, headers=headers)

        div_list = page.find_all('div', class_='hd')

        for div in div_list:
            title = div.a.span.text.strip()
            title_list.append(title)
        time.sleep(1)
    # print(title_list)
    doc = open('Top250Films_SingleThread.txt', 'w')
    for i in range(len(title_list)):
        print(title_list[i],file=doc)
    doc.close()

def main():
    t1 = time.time()
    download()
    t2 = time.time()

    print('*' * 50)
    print('Single thread downloading time：%s' % (t2-t1))
    print('*' * 50)

main()
