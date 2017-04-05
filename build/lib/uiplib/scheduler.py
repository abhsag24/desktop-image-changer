"""Module that schedules the wallpaper change."""

import os
import time
import sys
from select import select
import random

from uiplib.utils.utils import get_percentage
from uiplib.scrape import download

try:
    import msvcrt
except ImportError:
    # not on windows
    pass
from threading import Thread


class Scheduler:
    """Class which schedules the wallpaper change."""

    def __init__(self, offline, pics_folder, timeout, website, count,
                 skip_wallpaper, wallpaper, appObj=None):
        """Initialize the scheduler configuration."""
        self.website = website
        self.timeout = timeout
        self.directory = pics_folder
        self.count = count
        self.skip_wallpaper = skip_wallpaper
        self.wallpaper = wallpaper
        self.offline = offline
        self.appObj = appObj
        self.download_thread = None
        self.schedule_thread = None
        self.run()

    def change_random(self):
        """Change the wallpaper to a random image."""
        filename = random.choice(os.listdir(self.directory))
        path = os.path.join(self.directory, filename)
        print("changing desktop wallpaper to: ", path)
        self.wallpaper.set(path)

    def kbhit(self):
        """Return True if keyboard character was hit, False otherwise."""
        if not self.skip_wallpaper:
            return False
        if os.name == 'nt':
            return msvcrt.kbhit()
        else:
            dr, dw, de = select([sys.stdin], [], [], 0)
            return dr != []

    def getch(self):
        """Return a keyboard character after kbhit() has been called.

        Should not be called in the same program as getarrow().
        """
        if os.name == 'nt':
            return msvcrt.getch().decode('utf-8')
        else:
            return sys.stdin.read(1)

    def changeCycle(self):
        """Wallpaper change cycle."""
        uold, sold, cold, c, e = os.times()
        while True:
            if not self.kbhit():
                delta = self.deltaTime()
                if delta >= self.timeout:
                    self.change_random()
                    self.time = time.time()
            else:
                self.getch()
                print("Skipping this wallpaper")
                self.change_random()
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
        if not self.offline and not self.download_thread:
            self.download_thread = Thread(
                            target=download,
                            args=(self.website, self.directory, self.count),
                            kwargs={"appObj": self.appObj},
                            daemon=True)
            self.download_thread.start()

        elif not os.path.exists(self.directory):
            os.makedirs(self.directory)
            self.run()

        while os.listdir(self.directory) == []:  # Wait till first image.
            time.sleep(60)

        if not self.schedule_thread:
            print("You can wait for next wallpaper or skip this wallpaper"
                  " by just pressing enter.")
            self.change_random()
            self.setStartTime(time.time())
            self.schedule_thread = Thread(
                target=self.changeCycle,
                daemon=True)
            self.schedule_thread.start()
