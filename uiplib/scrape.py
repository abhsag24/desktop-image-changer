from bs4 import BeautifulSoup
from urllib import request
from urllib.request import urlopen
from urllib.request import urlretrieve
import os
import sys


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

def get_images(url, directory, count):
    '''
    scrape images from /r/wallpapers
    '''
    image_links = []
    p_url = url
    no_of_images = int(count)

    while len(image_links) < no_of_images:
        soup = make_soup(p_url)
        # this makes a list of bs4 element tags
        thumbnails = soup.find_all("a", class_="thumbnail", href=True)

        """Thumbnails in /r/wallpapers contain href to original
        full-sized image."""

        if not thumbnails:
            print('No matching image found')
            return

        for link in thumbnails:
            if link['href'].endswith(('jpg', 'png', 'jpeg', 'bmp')):
                image_links.append(link['href'])
            if(len(image_links) >= no_of_images):
                break

        # gets the link of next page
        p_url = soup.find("a", attrs={"rel" : "nofollow next"}).attrs['href']

    for image in image_links:
        if not os.path.exists(directory):
            os.makedirs(directory)
        filename = image.split('/')[-1]
        if filename not in os.listdir(directory):
            try:
                urlretrieve(image, os.path.join(
                    directory, filename), reporthook=dlProgress)
            except:
                pass
