from uiplib.setWallpaper import change_background
from uiplib.utils import get_percentage
from uiplib.scrape.onlineFetch import onlineFetch

import os
import time
from uiplib.scrape.scrape import get_images
from threading import Thread
import sys
from select import select
import random

try:
    import msvcrt
except ImportError:
    # not on windows
    pass


class scheduler():

    def __init__(self, offline, pics_folder, timeout, website, count, service):
        self.website = website
        self.timeout = timeout
        self.directory = pics_folder
        self.count = count
        self.service = service

        if not offline:
            try:
                thread_nos = len(self.website)
                for i in range(thread_nos):
                    # Init the thread
                    fetch_thread = onlineFetch(self.website[i],
                                               self.directory, self.count)
                    # die upon main thread exit
                    fetch_thread.setDaemon(True)

                    # Start new Threads
                    fetch_thread.start()

            except ValueError as e:
                print("File could not be retrieved.", e)

            while not ((os.path.isdir(self.directory) and
                        os.listdir(self.directory) != [])):
                print('Downloading images..')
                time.sleep(60)
        elif not os.path.exists(self.directory):
            os.makedirs(self.directory)

        if os.listdir(self.directory) != []:
            print("You can wait for next wallpaper or skip this wallpaper"
                  " by just pressing enter.")
            self.change_random()
            self.setStartTime(time.time())
            self.changeCycle()
        else:
            print("No downloaded images. Try again in online mode.")

    def change_random(self):
        filename = random.choice(os.listdir(self.directory))
        path = os.path.join(self.directory, filename)
        print("changing desktop wallpaper to: ", path)
        change_background(path)

    def kbhit(self):
        ''' Returns True if keyboard character was hit, False otherwise.
        '''
        if self.service:
            return False
        if os.name == 'nt':
            return msvcrt.kbhit()
        else:
            dr, dw, de = select([sys.stdin], [], [], 0)
            return dr != []

    def getch(self):
        ''' Returns a keyboard character after kbhit() has been called.
            Should not be called in the same program as getarrow().
        '''
        s = ''
        if os.name == 'nt':
            return msvcrt.getch().decode('utf-8')
        else:
            return sys.stdin.read(1)

    def changeCycle(self):
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
        self.time = time

    def deltaTime(self):
        return (time.time()-self.time)
