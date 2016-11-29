import unittest
import tempfile
import os
from uiplib import scrape

class ScrapeTest(unittest.TestCase):

    def test_get_image_links(self):
        old_reddit = scrape.get_reddit_image_links
        old_unsplash = scrape.get_unsplash_image_links
        scrape.get_unsplash_image_links = lambda x,y : [(1,1), (2,2)]
        scrape.get_reddit_image_links = lambda x,y : [(7,7), (8,8)]
        self.assertEqual(scrape.get_image_links(
                            'www.reddit.com/r/CoolSite', 2),
                         [(7, 7), (8, 8)])
        self.assertEqual(scrape.get_image_links(
                            'www.unsplash.com/new', 2),
                         [(1, 1), (2, 2)])
        scrape.get_reddit_image_links = old_reddit
        scrape.get_unsplash_image_links = old_unsplash

    def test_get_images(self):
        with tempfile.TemporaryDirectory() as directory:
            scrape.get_image_links =  lambda x,y : [('filename.png',
                'https://placeholdit.imgix.net/'
                '~text?txtsize=15&txt=image1&w=120&h=120')]
            scrape.get_images('url', directory, 1)
            self.assertEqual(os.listdir(directory), ['filename.png'])

    def test_reddit_image_links(self):
        scrape.make_json = lambda x  : {
                            'data' : {'children' : [{'data' : {'preview' : {
                              'images' : [{'source' : {'url' :
                                                    'url.com/some_url.png?21'}
                                }]}}}]}}
        self.assertEqual(scrape.get_reddit_image_links('url', 1),
                         [('some_url.png', 'url.com/some_url.png?21')])

