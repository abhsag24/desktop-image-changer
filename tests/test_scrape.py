import unittest
import tempfile
import os
from uiplib.scrape import scrape
from bs4 import BeautifulSoup


class ScrapeTest(unittest.TestCase):

    def setUp(self):
        self.json = {'data' : {'children' : [{'data' : {'preview' : {
                          'images' : [{'source' : {'url' :
                                'url.com/some_url.png?21'}}]}}}]}}
        self.html = ('<html><head></head><body><div class="y5w1y">'
                     '<div class="hduMF"><div class="_31wG7 _3YIV2">'
                     'Some text</div><div class="_114MZ"> Some text'
                     '</div><div class="_287Ma tPMQE"><a href="url.com'
                     '/photos/some_url/download?force=true"></a></div>'
                     '</div></div></body></html>')

    def test_get_image_links(self):
        old_reddit = scrape.get_reddit_image_links
        old_unsplash = scrape.get_unsplash_image_links
        scrape.get_unsplash_image_links = lambda x, y: [(1, 1), (2, 2)]
        scrape.get_reddit_image_links = lambda x, y: [(7, 7), (8, 8)]
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
            scrape.get_image_links = lambda x, y: [(
                  'filename.png',
                  'http://placeholdit.imgix.net/'
                  '~text?txtsize=15&txt=image1&w=120&h=120')]
            scrape.get_images('url', directory, 1)
            self.assertEqual(os.listdir(directory), ['filename.png'])

    def test_reddit_image_links(self):
        scrape.make_json = lambda x: {
                            'data': {'children': [{'data': {'preview': {
                              'images': [{'source': {'url':
                                                     'url.com/some_url.png?21'}
                                          }]}}}]}}
        self.assertEqual(scrape.get_reddit_image_links('url', 1),
                         [('some_url.png', 'url.com/some_url.png?21')])

        # No preview, sometimes children's list has no key Preview
        self.json['data']['children'].append({})
        self.assertEqual(scrape.get_reddit_image_links('url', 1),
                         [('some_url.png', 'url.com/some_url.png?21')])

        # No preview images
        json_1 = self.json
        json_1['data']['children'] = [{}]
        scrape.make_json = lambda x: json_1
        self.assertEqual(scrape.get_reddit_image_links('url', 1), [])

        # Bad Json, mostly in case of bad internet
        json_1 = self.json
        json_1['data'] = {}
        scrape.make_json = lambda x  : json_1
        self.assertEqual(scrape.get_reddit_image_links('url', 1), [])

    def test_unsplash_image_links(self):
        old_make_soup = scrape.make_soup
        scrape.make_soup = lambda x : BeautifulSoup(self.html, "html.parser")

        self.assertEqual(scrape.get_unsplash_image_links('url', 1),
                         [('some_url.jpg',
                           'url.com/photos/some_url/download?force=true')])

        # Bad html file, mostly in case of bad internet
        html = '<html></html>'
        scrape.make_soup = lambda x : BeautifulSoup(html, "html.parser")
        self.assertEqual(scrape.get_unsplash_image_links('url', 1), [])
        scrape.make_soup = old_make_soup

    def test_download(self):
        with tempfile.TemporaryDirectory() as directory:
            self.assertEqual(scrape.download_store_images(
                os.path.join(directory, 'filename.png'),
                'https://placeholdit.imgix.net/'
                '~text?txtsize=15&txt=image1&w=120&h=120'
            ), True)
            self.assertEqual(scrape.download_store_images(
                os.path.join(directory, 'filename.png'),
                'url'
            ), False)
