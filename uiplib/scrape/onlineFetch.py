from uiplib.scrape.scrape import get_images
from threading import Thread

# Class to create threads for get_images


class onlineFetch(Thread):

    def __init__(self, url, directory, count):
        Thread.__init__(self)
        self.url = url
        self.directory = directory
        self.count = count

    def run(self):
        get_images(self.url, self.directory, self.count)
