from bs4 import BeautifulSoup
from urllib import request
from urllib.request import urlopen
from urllib.request import urlretrieve
import os
import sys
from uiplib.constants import (PICS_FOLDER,
                              NUMBER_OF_IMAGES_TO_PARSE,
                              CURR_DIR,
                              PICS_FOLDER)


def make_soup(url):
    '''
    makes soup, that is basically parsing the html document
    '''
    req = request.Request(url=url, headers={
                          'User-Agent': ' Mozilla/5.0'
                                        ' (Windows NT 6.1; WOW64; rv:12.0)'
                                        ' Gecko/20100101 Firefox/12.0'})
    response = request.urlopen(req)
    html = response.read()
    return BeautifulSoup(html, "html.parser")


def dlProgress(count, blockSize, totalSize):
    '''
    Show Progress bar
    '''
    percent = int(count*blockSize*100/totalSize)
    sys.stdout.write("\r" + "...%d%%" % percent)
    sys.stdout.flush()


def get_images(url):
    '''
    scrape images from /r/wallpapers
    '''
    soup = make_soup(url)
    # this makes a list of bs4 element tags
    thumbnails = soup.find_all("a", class_="thumbnail", href=True)

    """Thumbnails in /r/wallpapers contain href to original
    full-sized image."""

    image_links = []
    if not thumbnails:
        print('No matching image found')
        return

    for link in thumbnails:
        if link['href'].endswith(('jpg', 'png', 'jpeg', 'bmp')):
            image_links.append(link['href'])
        if(len(image_links) == NUMBER_OF_IMAGES_TO_PARSE):
            break

    for image in image_links:
        path = os.path.join(CURR_DIR, PICS_FOLDER)
        if not os.path.exists(path):
            os.makedirs(path)
        filename = image.split('/')[-1]
        if filename not in os.listdir(path):
            try:
                urlretrieve(image, os.path.join(
                    path, filename), reporthook=dlProgress)
            except:
                pass
