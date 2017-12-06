"""Module that scrapes the wallpapers."""

import os
import sys
import json
from urllib.request import urlretrieve, getproxies

import requests
from bs4 import BeautifulSoup


def make_soup(url):  # pragma: no cover
    """Make soup, that is basically parsing the html document."""
    response = requests.get(
        url,
        headers={'User-agent': 'UIP'},
        # gets system proxy (if it is currently using one)
        proxies=getproxies())

    html = response.content
    return BeautifulSoup(html, "html.parser")


def make_json(url):  # pragma: no cover
    """Make a dictionary out of a json file."""
    response = requests.get(
        url,
        headers={'User-agent': 'UIP'},
        # gets system proxy (if it is currently using one)
        proxies=getproxies())

    json_file = response.text
    data = json.loads(json_file)
    return data


def dlProgress(count, blockSize, totalSize):
    """Show Progress bar."""
    percent = int(count*blockSize*100/totalSize)/2
    sys.stdout.write("\r[%s%s]" % ('='*int(percent), ' '*(50-int(percent))))
    sys.stdout.flush()


def get_unsplash_image_links(url):
    """Retrieve images from unsplash.

    Returns a list of tuples containing filename and url of the image.
    """
    soup = make_soup(url)
    '''Selects desired bs4 tags, soup.select is a recursive function,
       it searches for classes/tags within classes/tags'''
    no_of_images = 5
    a_tags = soup.select('.y5w1y .hduMF .tPMQE a')
    image_links = []
    if not a_tags:
        print('No matching image found')
        return []

    for a_tag in a_tags:
        image_url = a_tag['href']
        filename = image_url.split('/')[-2] + ".jpg"
        image_links.append({
                            'name': filename,
                            'image_url': image_url
                           })
        if len(image_links) < no_of_images:
            break
    return image_links


def get_reddit_image_links(url):
    """Retrieve images from reddit.

    Returns a list of tuples containing filename and url of the image.
    """
    # reddit requires .json format for the URL
    no_of_images = 5
    page = make_json(url + '/.json')
    image_links = []
    children = []
    try:
        # structure of reddit API
        children = page['data']['children']
    except (IndexError, KeyError) as e:
        print("You seem to be having some issues with your internet."
              "Please contact us at our github repo 'NIT-dgp/UIP'"
              "If you feel it isn't the case with your internet.", e)
    for child in children:
        images = []
        try:
            images = child['data']['preview']['images']
        except KeyError:
            pass

        for image in images:
            if(len(image_links) < no_of_images):
                image_url = image['source']['url']
                filename = image_url.split('/')[-1]
                filename = filename[: filename.find('?')]
                image_links.append({
                                    'name': filename,
                                    'image_url': image_url
                                   })

    return image_links


def get_desktoppr_image_links(url):
    """Retrieve images from desktoppr.

    Returns a list of tuples containing filename and url of the image.
    """
    no_of_images = 5
    responses = []
    image_links = []
    index = 1

    while len(responses) < no_of_images:
        page_url = url + ('?page=%d' % index)
        data = make_json(page_url)
        responses.extend(data['response'])
        index += 1

    responses = responses[:no_of_images]

    for result in responses:
        image_url = result['image']['url']
        filename = image_url.split('/')[-1]
        image_links.append({
                            'name': filename,
                            'image_url': image_url
                           })

    return image_links


def get_image_data_list(websites):
    """Return the links for images."""
    image_links = []
    for url in websites:
        if 'unsplash' in url:  # For Unsplash
            image_links.extend(get_unsplash_image_links(url))

        elif 'reddit' in url:  # For Reddit
            image_links.extend(get_reddit_image_links(url))

        elif 'desktoppr' in url:  # For Desktoppr
            image_links.extend(get_desktoppr_image_links(url))

    return image_links


def download_and_store_image(directory, image_data):
    """Download and store the images to the specified path."""
    try:
        urlretrieve(image_data.get('image_url'),
                    os.path.join(directory, image_data.get('name')),
                    reporthook=dlProgress)
        return True
    except Exception as e:
        print(image_data.get('image_url'))
        print("Image cannot be downloaded: ", str(e))
        return False
