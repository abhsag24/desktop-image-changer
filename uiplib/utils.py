import os
import sys
import time
from uiplib.scrape import get_images
from threading import Thread
from uiplib.settings import HOME_DIR
from daemoniker import send, SIGTERM


def get_percentage(unew, uold, start):
    del_time = (time.time()-float(start))
    if del_time != 0:
        return 100 * ((float(unew) - float(uold)) / del_time)
    return 100


def make_dir(dirpath):
    os.makedirs(dirpath)
    if sys.platform.startswith('linux'):
        os.chmod(dirpath, 0o777)


def exit_UIP():
    pid_file = os.path.join(HOME_DIR, 'daemon-uip.pid')
    if os.path.exists(pid_file):
        send(pid_file, SIGTERM)
        os.remove(pid_file)
    print("\nExiting UIP hope you had a nice time :)")
    sys.exit(0)

# Class to create threads for get_images


class onlineFetch(Thread):

    def __init__(self, url, directory, count):
        Thread.__init__(self)
        self.url = url
        self.directory = directory
        self.count = count

    def run(self):
        get_images(self.url, self.directory, self.count)


def check_version():
    """Check for the version of python interpreter"""
    # Required version of python interpreter
    req_version = (3, 5)
    # Current version of python interpreter
    curr_version = sys.version_info

    # Exit if minimum requirements are not met
    if curr_version < req_version:
        raise SystemExit("Your python interpreter does not meet" +
                         " the minimum requirements.\n" +
                         "Consider upgrading to python3.5")
