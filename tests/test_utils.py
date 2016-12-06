import os
import sys
import shutil
import unittest
from uiplib.utils import make_dir

class UtilsTest(unittest.TestCase):

    def test_make_dir(self):
        testdir = os.path.join(os.path.expanduser("~"), '.test')
        make_dir(testdir)
        self.assertTrue(os.path.exists(testdir))
        if sys.platform.startswith('linux'):
            self.assertEqual(oct(os.stat(testdir).st_mode)[-3:],'777')
        shutil.rmtree(testdir)
