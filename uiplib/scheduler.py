from uiplib.setWallpaper import change_background
import os
import random
import time
from uiplib.scrape import get_images
from threading import Thread
import sys
from select import select
try:
    import msvcrt
except ImportError:
    #msvcrt module is only available on windows
    pass

class scheduler():

    def __init__(self, offline, pics_folder, timout, website, count):
        self.website = website
        self.timeout = timout
        self.directory = pics_folder
        self.count = count
        if not offline:
            fetch = Thread(target=self.initFetch)
            # all child threads need to be daemons to die upon main thread exit
            fetch.setDaemon(True)
            fetch.start()
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

    def initFetch(self):
        try:
            get_images(self.website, self.directory, self.count)
        except ValueError as e:
            print("File could not be retrieved.", e)

    def change_random(self):
        filename = random.choice(os.listdir(self.directory))
        path = os.path.join(self.directory, filename)
        print("changing desktop wallpaper to: ", path)
        change_background(path)

    def kbhit(self):
        ''' Returns True if keyboard character was hit, False otherwise.
        '''
        if os.name == 'nt':
            return msvcrt.kbhit()
        else:
            dr,dw,de = select([sys.stdin], [], [], 0)
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
        while True:
            if self.kbhit() and self.getch() == 's':
                print("Skipping this wallpaper")
                self.change_random()
                self.time = time.time()
            else:
                delta = self.deltaTime()
                if delta >= self.timeout:
                    self.change_random()
                    self.time = time.time()

    def setStartTime(self, time):
        self.time = time

    def deltaTime(self):
        return (time.time()-self.time)
