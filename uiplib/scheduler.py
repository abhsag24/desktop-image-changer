"""Module that schedules the wallpaper change."""

import os
import time
from select import select
import random

from uiplib.utils.utils import get_percentage
from uiplib.scrape import get_image_data_list
from uiplib.scrape import download_and_store_image

try:
    import msvcrt
except ImportError:
    # not on windows
    pass


class Scheduler:
    """Class which schedules the wallpaper change."""

    def __init__(self, pics_folder, timeout, website, wallpaper):
        """Initialize the scheduler configuration."""
        self.website = website
        self.timeout = timeout
        self.directory = pics_folder
        self.wallpaper = wallpaper
        self.schedule_thread = None
        self.image_data_list = []
        self.run()

    def change_next(self):
        """Change the wallpaper to the next image."""
        prev_wallpaper_path = self.wallpaper.get()[0]
        next_wallpaper_data = self.get_next_wallpaper()
        download_and_store_image(self.directory,
                                 next_wallpaper_data)
        path = os.path.join(self.directory,
                            next_wallpaper_data.get('name'))
        if os.path.exists(path):
            self.wallpaper.set(path)
        if os.path.exists(prev_wallpaper_path):
            os.remove(prev_wallpaper_path)

    def get_next_wallpaper(self):
        """Get next image to be downloaded."""
        if not len(self.image_data_list) == 0:
            return self.image_data_list.pop()
        else:
            # get fresh links
            self.image_data_list = get_image_data_list(self.website)
            random.shuffle(self.image_data_list)
            print(self.image_data_list)
            return self.image_data_list.pop()

    def changeCycle(self):
        """Wallpaper change cycle."""
        uold, sold, cold, c, e = os.times()
        while True:
            delta = self.deltaTime()
            if delta >= self.timeout:
                self.change_next()
                self.time = time.time()
            unew, snew, cnew, c, e = os.times()
            start = time.time()
            percentage = get_percentage(unew, uold, start)
            if percentage > 30.0:
                time.sleep(0.1)

    def setStartTime(self, time):
        """Set the start time."""
        self.time = time

    def deltaTime(self):
        """Return the time difference."""
        return (time.time()-self.time)

    def run(self):
        """Begin Scheduling Wallpapers."""
        self.change_next()
        self.setStartTime(time.time())
        self.changeCycle()
