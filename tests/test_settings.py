import unittest
from unittest.mock import patch

from uiplib import settings


class SettingsTest(unittest.TestCase):

    def setUp(self):
        with patch('sys.argv', new=['UIP']):
            self.parseSettings = settings.ParseSettings()

    def test_get_settings_from_cli(self):

        # No of images and offline should not be mixed
        args = ['UIP', '--no-of-images', '20', '--offline']
        with patch('sys.argv', new=args):
            settings = self.parseSettings.get_settings_from_cli()
            self.assertIsNotNone(settings['error'])

        # Test no-of-images
        args = ['UIP', '--no-of-images', '20']
        with patch('sys.argv', new=args):
            settings = self.parseSettings.get_settings_from_cli()
            self.assertEqual(settings['no-of-images'], '20')

        # Test service
        args = ['UIP', '--service', 'stop']
        with patch('sys.argv', new=args):
            settings = self.parseSettings.get_settings_from_cli()
            self.assertEqual(settings['service'], 'stop')

        # Test offline and flush together
        args = ['UIP', '--offline', '--flush']
        with patch('sys.argv', new=args):
            settings = self.parseSettings.get_settings_from_cli()
            self.assertEqual(settings['offline'], True)
            self.assertEqual(settings['flush'], True)

        # Test invalid option
        with self.assertRaises(SystemExit):
            args = ['UIP', '--something']
            with patch('sys.argv', new=args):
                settings = self.parseSettings.get_settings_from_cli()
