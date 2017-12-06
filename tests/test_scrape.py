import unittest

from bs4 import BeautifulSoup

from uiplib import scrape


class ScrapeTest(unittest.TestCase):

    def setUp(self):
        self.json = {'data': {'children': [{'data': {'preview': {
                          'images': [{'source':
                                      {'url':
                                       'url.com/some_url.png?21'}}]}}}]}}
        self.html = ('<html><head></head><body><div class="y5w1y">'
                     '<div class="hduMF"><div class="_31wG7 _3YIV2">'
                     'Some text</div><div class="_114MZ"> Some text'
                     '</div><div class="_287Ma tPMQE"><a href="url.com'
                     '/photos/some_url/download?force=true"></a></div>'
                     '</div></div></body></html>')

    def test_get_image_data_list(self):
        old_reddit = scrape.get_reddit_image_links
        old_unsplash = scrape.get_unsplash_image_links
        old_desktoppr = scrape.get_desktoppr_image_links
        scrape.get_unsplash_image_links = \
            lambda x: [
                {'name': 1, 'image_url': 1},
                {'name': 2, 'image_url': 2}]
        scrape.get_reddit_image_links = \
            lambda x: [
                {'name': 7, 'image_url': 7},
                {'name': 8, 'image_url': 8}]
        scrape.get_desktoppr_image_links = \
            lambda x: [
                {'name': 3, 'image_url': 3},
                {'name': 4, 'image_url': 4}]

        self.assertEqual(
          scrape.get_image_data_list(
              ['www.reddit.com/r/CoolSite']),
          [{'name': 7, 'image_url': 7}, {'name': 8, 'image_url': 8}])
        self.assertEqual(
          scrape.get_image_data_list(
              ['www.unsplash.com/new']),
          [{'name': 1, 'image_url': 1},
           {'name': 2, 'image_url': 2}])
        self.assertEqual(
          scrape.get_image_data_list(
              ['api.desktoppr.co/1/wallpapers']),
          [{'name': 3, 'image_url': 3}, {'name': 4, 'image_url': 4}])

        scrape.get_reddit_image_links = old_reddit
        scrape.get_unsplash_image_links = old_unsplash
        scrape.get_desktoppr_image_links = old_desktoppr

    def test_reddit_image_links(self):
        scrape.make_json = lambda x: {
            'data': {'children': [{'data': {'preview': {
                'images': [{'source':
                            {'url':
                             'url.com/some_url.png?21'}}]}}}]}}
        self.assertEqual(
          scrape.get_reddit_image_links('url'),
            [{'name': 'some_url.png',
              'image_url': 'url.com/some_url.png?21'}])

        # No preview, sometimes children's list has no key Preview
        self.json['data']['children'].append({})
        self.assertEqual(
          scrape.get_reddit_image_links('url'),
            [{'name': 'some_url.png',
              'image_url': 'url.com/some_url.png?21'}])

        # No preview images
        json_1 = self.json
        json_1['data']['children'] = [{}]
        scrape.make_json = lambda x: json_1
        self.assertEqual(scrape.get_reddit_image_links('url'), [])

        # Bad Json, mostly in case of bad internet
        json_1 = self.json
        json_1['data'] = {}
        scrape.make_json = lambda x: json_1
        self.assertEqual(scrape.get_reddit_image_links('url'), [])

    def test_unsplash_image_links(self):
        old_make_soup = scrape.make_soup
        scrape.make_soup = lambda x: BeautifulSoup(self.html, "html.parser")
        self.assertEqual(
          scrape.get_unsplash_image_links('url'),
          [{'name': 'some_url.jpg',
            'image_url': 'url.com/photos/some_url/download?force=true'}])

        # Bad html file, mostly in case of bad internet
        html = '<html></html>'
        scrape.make_soup = lambda x: BeautifulSoup(html, "html.parser")
        self.assertEqual(scrape.get_unsplash_image_links('url'), [])
        scrape.make_soup = old_make_soup

    def test_desktoppr_image_links(self):
        scrape.make_json = lambda x: {
            'response': [{
                    'image': {
                        'url': 'example.com/example.jpg'
                    }
            }]
        }

        self.assertEqual(
          scrape.get_desktoppr_image_links('url'),
          [{'name': 'example.jpg', 'image_url': 'example.com/example.jpg'},
           {'name': 'example.jpg',
            'image_url': 'example.com/example.jpg'},
           {'name': 'example.jpg',
            'image_url': 'example.com/example.jpg'},
           {'name': 'example.jpg',
            'image_url': 'example.com/example.jpg'},
           {'name': 'example.jpg', 'image_url': 'example.com/example.jpg'}])
