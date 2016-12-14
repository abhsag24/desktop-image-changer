"""Module that scrapes the wallpapers."""

from bs4 import BeautifulSoup
import requests
from urllib.request import urlretrieve
import os
import sys
import json


def make_soup(url):  # pragma: no cover
    """Make soup, that is basically parsing the html document."""
    response = requests.get(url, headers={'User-agent': 'UIP'})
    html = response.content
    return BeautifulSoup(html, "html.parser")


def make_json(url):  # pragma: no cover
    """Make a dictionary out of a json file."""
    response = requests.get(url, headers={'User-agent': 'UIP'})
    json_file = response.text
    data = json.loads(json_file)
    return data


def dlProgress(count, blockSize, totalSize):
    """Show Progress bar."""
    percent = int(count*blockSize*100/totalSize)/2
    sys.stdout.write("\r[%s%s]" % ('='*int(percent), ' '*(50-int(percent))))
    sys.stdout.flush()


def get_unsplash_image_links(url, no_of_images):
    """Retrieve images from unsplash.

    Returns a list of tuples containing filename and url of the image.
    """
    soup = make_soup(url)
    '''Selects desired bs4 tags, soup.select is a recursive function,
       it searches for classes/tags within classes/tags'''
    a_tags = soup.select('.y5w1y .hduMF .tPMQE a')
    image_links = []
    if not a_tags:
        print('No matching image found')
        return

    for a_tag in a_tags:
        image_url = a_tag['href']
        filename = image_url.split('/')[-2]+".jpg"
        image_links.append((filename, image_url))
        if(len(image_links) >= no_of_images):
            break

    return image_links


def get_reddit_image_links(url, no_of_images):
    """Retrieve images from reddit.

    Returns a list of tuples containing filename and url of the image.
    """
    # reddit requires .json format for the URL
    page = make_json(url+'/.json')
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
                image_links.append((filename, image_url))

    return image_links


def get_desktoppr_image_links(url, no_of_images):
    """Retrieve images from desktoppr.

    Returns a list of tuples containing filename and url of the image.
    """
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
        image_links.append((filename, image_url))

    return image_links


def get_image_links(url, count):
    """Return the links for images."""
    image_links = []

    if 'unsplash' in url:  # For Unsplash
        image_links.extend(get_unsplash_image_links(url, count))

    elif 'reddit' in url:  # For Reddit
        image_links.extend(get_reddit_image_links(url, count))

    elif 'desktoppr' in url:  # For Desktoppr
        image_links.extend(get_desktoppr_image_links(url, count))

    return image_links


def download_store_images(full_path, image_link):  # pragma no-cover
    """Download and store the images to the specified path."""
    try:
        urlretrieve(image_link,
                    full_path,
                    reporthook=dlProgress)
    except Exception as e:
        print("Image cannot be downloaded: ", str(e))


def get_images(url, directory, count):
    """Scrape images from a URL into a directory."""
    no_of_images = int(count)
    image_links = get_image_links(url, no_of_images)
    for image in image_links:
        download_store_images(os.path.join(directory, image[0]), image[1])
