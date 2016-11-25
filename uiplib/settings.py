import os
import json, argparse

HOME_DIR = os.path.join(os.path.expanduser("~"), '.uip')
NUMBER_OF_IMAGES_TO_PARSE = 15
DEFAULT_PICS_FOLDER = os.path.join(HOME_DIR, 'pics')

settings_file_path = os.path.join(HOME_DIR, "settings.json")

class ParseSettings:

    def __init__(self):
        self.settings = self.get_settings_from_file()
        self.settings.update(self.get_settings_from_cli())

    def get_settings_from_file(self):
        with open(settings_file_path, "r") as settings_file:
            settings = json.loads(settings_file.read())
        return settings

    def get_settings_from_cli(self):
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
        args = self.parser.parse_args()

        settings = {
            'service' : args.service,
            'offline': args.offline,
            'flush': args.flush,
            'error': args.no_of_images and args.offline,
        }
        if args.no_of_images:
            settings['no-of-images'] = args.no_of_images

        return settings

    def show_help(self):
        self.parser.print_help()

