import time
from uiplib.scrape import get_images
from threading import Thread

def get_percentage(unew, uold, start):
    del_time = (time.time()-float(start))
    if del_time != 0:
        return 100 * ((float(unew) - float(uold)) / del_time)
    return 100


#Class to create threads for get_images
class onlineFetch(Thread):
    def __init__(self, url, directory, count):
        Thread.__init__(self)
        self.url = url
        self.directory = directory
        self.count = count

    def run(self):
        get_images(self.url, self.directory, self.count)
