import os
import sys
import shutil
import unittest
import time
from uiplib.utils import setupUtils, utils
from uiplib.settings import DEFAULT_PICS_FOLDER, NUMBER_OF_IMAGES_TO_PARSE


class UtilsTest(unittest.TestCase):

    def test_make_dir(self):
        testdir = os.path.join(os.path.expanduser("~"), '.test')
        setupUtils.make_dir(testdir)
        self.assertTrue(os.path.exists(testdir))
        if sys.platform.startswith('linux'):
            self.assertEqual(oct(os.stat(testdir).st_mode)[-3:], '777')
        shutil.rmtree(testdir)

    def test_get_percentage(self):
        self.assertLessEqual(utils.get_percentage(1, 0, 0), 100)
        self.assertGreaterEqual(utils.get_percentage(1, 0, time.time()), 0)

    def test_check_version(self):
        self.assertGreaterEqual(setupUtils.get_current_version(), (3, 5))
        with self.assertRaises(SystemExit):
            setupUtils.get_current_version = lambda: (0, 0)
            setupUtils.check_version()

    def test_check_sites(self):
        self.assertEqual(utils.check_sites({
                'website': [
                    'https://unsplash.com/new',
                    'https://www.reddit.com/r/wallpapers/',
                    'https://www.reddit.com/r/wallpaper/',
                    'https://www.reddit.com/r/EarthPorn/',
                    'https://www.reddit.com/r/VillagePorn/',
                    'https://www.reddit.com/r/pics/',
                    'https://api.desktoppr.co/1/wallpapers', ]}),
                {
                    'desktoppr': True,
                    'unsplash': True,
                    'reddit': [
                        'https://www.reddit.com/r/wallpapers/',
                        'https://www.reddit.com/r/wallpaper/',
                        'https://www.reddit.com/r/EarthPorn/',
                        'https://www.reddit.com/r/VillagePorn/',
                        'https://www.reddit.com/r/pics/'
                    ]
                })
