"""Module to fetch wallpapers."""

from uiplib.scrape.scrape import get_images
from threading import Thread


class onlineFetch(Thread):
    """Generic thread module to download images."""

    def __init__(self, url, directory, count):
        """Initialize the fetch thread."""
        Thread.__init__(self)
        self.url = url
        self.directory = directory
        self.count = count

    def run(self):
        """Begin the download. Automatically called when a thread starts."""
        get_images(self.url, self.directory, self.count)
