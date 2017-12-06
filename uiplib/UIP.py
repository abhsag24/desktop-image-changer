"""Main UIP Module."""

import time

from daemoniker import Daemonizer

from uiplib.settings import HOME_DIR
from uiplib.settings import ParseSettings
from uiplib.scheduler import Scheduler
from uiplib.Wallpaper import Wallpaper
from uiplib.utils.utils import exit_UIP
from uiplib.utils.utils import flush_wallpapers


def main():
    """Main method of the UIP."""
    wallpaper = Wallpaper()
    settingsParser = ParseSettings()
    settings = settingsParser.settings
    try:
        scheduler_object = Scheduler(settings['pics-folder'],
                                     settings['timeout'],
                                     settings['website'],
                                     wallpaper)
        while True:  # To keep the program from closing.
            time.sleep(15)
    except KeyboardInterrupt:
        exit_UIP()
