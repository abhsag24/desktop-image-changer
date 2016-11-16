from  setWallpaper import change_background
import os
from constants import CURR_DIR,PICS_FOLDER,WEBSITE,TIMEOUT
import random
import time
from scrape import get_images
from threading import Thread
class scheduler():
    def __init__(self):
        print (time.time())
        fetch = Thread(target=self.initFetch)
        fetch.start()
        while not os.path.isdir(os.path.join(CURR_DIR,PICS_FOLDER)):
            print('Downloading images..')
            time.sleep(60)
        self.change_random()
        self.setStartTime(time.time())
        self.changeCycle()
        
    def initFetch(self):
        try:    
            get_images(WEBSITE)
        except ValueError as e:
            print("File could not be retrieved.", e)

    def change_random(self):
        directory = os.path.join(CURR_DIR,PICS_FOLDER)
        filename = random.choice(os.listdir(directory))
        path = os.path.join(directory, filename)
        print("changing desktop wallpaper to: " ,path)
        change_background(path)

    def changeCycle(self):
        while True:
            delta = self.deltaTime()
            if delta>=TIMEOUT:
                self.change_random()
                self.time=time.time()
        
            else:
                time.sleep(TIMEOUT-delta)

            
    def setStartTime(self,time):
        self.time=time

    def deltaTime(self):
        return (time.time()-self.time)

    def checkTime(self):
        if self.deltaTime()>30:
            return True
        return False
