from bs4 import BeautifulSoup
import requests
from urllib.request import urlretrieve
import os
import sys
import json

def make_soup(url):
    '''
    makes soup, that is basically parsing the html document
    '''
    response = requests.get(url, headers = {'User-agent': 'UIP'})
    html = response.content
    return BeautifulSoup(html, "html.parser")

def make_json(url):
    """
    makes a dictionary out of a json file. If API like: URL/.json
    """
    response = requests.get(url + '/.json', headers = {'User-agent': 'UIP'})
    json_file = response.text
    data = json.loads(json_file)
    return data


def dlProgress(count, blockSize, totalSize):
    '''
    Show Progress bar
    '''
    percent = int(count*blockSize*100/totalSize)/2
    sys.stdout.write("\r[%s%s]" % ('='*int(percent), ' '*(50-int(percent))))
    sys.stdout.flush()

def get_images(url, directory, count):
    '''
    scrape images from /r/wallpapers
    '''
    image_links = []
    no_of_images = int(count)

    if 'unsplash' in url:       #For Unsplash
        soup = make_soup(url)
        '''Selects desired bs4 tags, soup.select is a recursive function,
           it searches for classes/tags within classes/tags'''
        a_tags = soup.select('.y5w1y .hduMF .tPMQE a')

        if not a_tags:
            print ('No matching image found')
            return

        for a_tag in a_tags:
            image_links.append(a_tag['href'])
            if(len(image_links) >= no_of_images):
                break

    elif 'reddit' in url:     #For Reddit
        page = make_json(url)
        try:
            for sub in page['data']['children']: # structure of reddit API
                for image in sub['data']['preview']['images']:
                    if(len(image_links)<no_of_images):
                        image_links.append(image['source']['url'])
        except (IndexError, KeyError) as e:
            print("You seem to be having some issues with your internet."
                  "Please contact us at our github repo 'NIT-dgp/UIP'"
                  "If you feel it isn't the case with your internet.")


    for image in image_links:
        if not os.path.exists(directory):
            os.makedirs(directory)
        if  'unsplash' in url:    #Unsplash
            filename = image.split('/')[-2]+".jpg"
        elif 'reddit' in url:     #Reddit
            filename = image.split('/')[-1]
            filename = filename[: filename.find('?')]

        try:
            urlretrieve(image,
                        os.path.join(directory,filename),
                        reporthook = dlProgress)
        except Exception as e:
            print("Image cannot be downloaded: ",str(e))
