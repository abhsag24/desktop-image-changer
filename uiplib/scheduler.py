from uiplib.setWallpaper import change_background
import os
from constants import CURR_DIR, PICS_FOLDER, WEBSITE, TIMEOUT
import random
import time
from uiplib.scrape import get_images
from threading import Thread


class scheduler():

    def __init__(self, offline):
        directory = os.path.join(CURR_DIR, PICS_FOLDER)
        print(time.time())
        if not offline:
            fetch = Thread(target=self.initFetch)
            # all child threads need to be daemons to die upon main thread exit
            fetch.setDaemon(True)
            fetch.start()
            while not (os.path.isdir(os.path.join(CURR_DIR, PICS_FOLDER)) and os.listdir(directory)!=[]):
                print('Downloading images..')
                time.sleep(60)
        elif not os.path.exists(directory):
            os.makedirs(directory)

        if os.listdir(directory) != []:
            self.change_random()
            self.setStartTime(time.time())
            self.changeCycle()
        else:
            print("No downloaded images. Try again in online mode.")

    def initFetch(self):
        try:
            get_images(WEBSITE)
        except ValueError as e:
            print("File could not be retrieved.", e)

    def change_random(self):
        directory = os.path.join(CURR_DIR, PICS_FOLDER)
        filename = random.choice(os.listdir(directory))
        path = os.path.join(directory, filename)
        print("changing desktop wallpaper to: ", path)
        change_background(path)

    def changeCycle(self):
        while True:
            delta = self.deltaTime()
            if delta >= TIMEOUT:
                self.change_random()
                self.time = time.time()

            else:
                time.sleep(TIMEOUT-delta)

    def setStartTime(self, time):
        self.time = time

    def deltaTime(self):
        return (time.time()-self.time)

    def checkTime(self):
        if self.deltaTime() > 30:
            return True
        return False
