import os
import requests
import urllib.request
from bs4 import BeautifulSoup

def get_page(url, params=None, headers=None):
    response = requests.get(url, headers=headers, params=params)
    page = BeautifulSoup(response.text, 'lxml')
    print(response.url)
    print("response status code", response.status_code)
    return page

def download_picture():
    value = ["NOW_PLAYING", "COMING_SOON", "ON_DEMAND"]
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.83 Safari/537.36',
        'Host': 'www.amctheatres.com'
    }
    for i in range(3):
        params = {"availability" : value[i]}
        page = get_page('https://www.amctheatres.com/movies', params=params, headers=headers)

        pic_content_list = page.find_all('div', class_='Slide')
        images = [pic_content.find('img') for pic_content in pic_content_list]
        picture_link_list = [image['src'] for image in images]

        name_content_list = page.find_all('div', class_='PosterContent')
        names = [name_content.find('h3') for name_content in name_content_list]
        picture_name_list = [name.get_text() for name in names]
        
        for picture_name, picture_link in zip(picture_name_list, picture_link_list):
            urllib.request.urlretrieve(picture_link, './AMCMovies/%s.jpg' % picture_name)

def mkdir(path):
	folder = os.path.exists(path)
	if not folder:                   
		os.makedirs(path)            
		print("Create new directory: %s" % path)		

def main():
    file_name = "AMCMovies"
    mkdir(file_name)
    download_picture()
    print("Download sucesseful!")

main()