"""Module that configures the settings for UIP."""

import os
import json
import argparse

HOME_DIR = os.path.join(os.path.expanduser("~"), '.uip')
NUMBER_OF_IMAGES_TO_PARSE = 15
DEFAULT_PICS_FOLDER = os.path.join(HOME_DIR, 'pics')
DEFAULT_FAVOURITE_PICS_FOLDER = os.path.join(HOME_DIR, 'favourite_pics')
DEFAULT_SETTINGS = {'timeout': 30*60,
                    'no-of-images': NUMBER_OF_IMAGES_TO_PARSE,
                    'pics-folder': DEFAULT_PICS_FOLDER,
                    'fav-pics-folder': DEFAULT_FAVOURITE_PICS_FOLDER,
                    'days-to-autodel': 10*24*60*60,
                    'website': ['https://unsplash.com/new',
                                'https://www.reddit.com/r/wallpapers/',
                                'https://www.reddit.com/r/wallpaper/',
                                'https://www.reddit.com/r/EarthPorn/',
                                'https://www.reddit.com/r/VillagePorn/',
                                'https://www.reddit.com/r/pics/',
                                'https://api.desktoppr.co/1/wallpapers', ]}

settings_file_path = os.path.join(HOME_DIR, "settings.json")


class ParseSettings:
    """Argument Parser class."""

    def __init__(self):
        """Initialize the argument parser."""
        self.settings = self.get_settings_from_file()
        self.settings.update(self.get_settings_from_cli())

    def get_settings_from_file(self):
        """Return the settings from file."""
        with open(settings_file_path, "r") as settings_file:
            settings = json.loads(settings_file.read())
        return settings

    def get_settings_from_cli(self):
        """Return the settings from system arguments."""
        self.parser = argparse.ArgumentParser()
        self.parser.add_argument("--offline", action="store_true",
                                 help="Runs UIP in offline mode.")
        self.parser.add_argument("--service",
                                 help="Run UIP as a service, "
                                      "--service start: to start UIP, "
                                      "--service stop: to stop UIP\n")
        self.parser.add_argument("--flush", action="store_true",
                                 help="Delete all downloaded wallpapers"
                                 " and downloads new ones. "
                                 "When combined with --offline,"
                                 " deletes the wallpapers and exits.")
        self.parser.add_argument("--no-of-images",
                                 help="Specify the no. of images to be "
                                 "downloaded. This should not be "
                                 "combined with --offline flag.")
        self.parser.add_argument("--ui", action="store_true",
                                 help="Start the app in Graphical "
                                 "Interface mode. This should not be"
                                 "combined with --service flag.")
        args = self.parser.parse_args()

        settings = {
            'service': args.service,
            'offline': args.offline,
            'flush': args.flush,
            'error': (args.no_of_images and args.offline) or
                     (args.ui and args.service),
            'ui': args.ui,
        }
        if args.no_of_images:
            settings['no-of-images'] = args.no_of_images

        return settings

    def show_help(self):  # pragma: no cover
        """Method to display the argument help."""
        self.parser.print_help()
