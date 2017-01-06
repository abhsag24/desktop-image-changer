"""Module that builds the Graphical User Interface."""

import os
from queue import Queue
from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox
from threading import Thread, active_count
from shutil import copy

from uiplib.gui import generalTab, settingsTab
from uiplib.scheduler import scheduler
from uiplib.utils.utils import flush_wallpapers
from uiplib.settings import DEFAULT_FAVOURITE_PICS_FOLDER
from uiplib.scrape import download


class MainWindow:
    """The main window that houses the app."""

    def __init__(self, settings, wallpaper):
        """Initialize the Main Window."""
        # configuration
        self.settings = settings
        # base window
        self.root = Tk()
        self.root.resizable(width=False, height=False)
        # set window title
        self.root.title("UIP")
        # self.root.wm_iconbitmap() sets icon bitmap
        self.queue = Queue()
        self.index = 0
        self.images = []
        self.update_images()
        # create the UI
        self.create_ui()
        self.wallpaper = wallpaper
        self.scheduler_object = None

    def create_ui(self):
        """Method to initialize UI."""
        self.notebook = Notebook(self.root)
        self.notebook.pack()
        generalTab.create_general_tab(self)
        settingsTab.create_settings_tab(self)

    def show_progess(self, show):
        """Method to display download progress."""
        if show:
            self.progressBar = Progressbar(self.headerFrame,
                                           orient=HORIZONTAL,
                                           length='300',
                                           variable=self.progress,
                                           mode='determinate')
            self.progressBar.pack(fill=BOTH, padx=5, pady=5)
        else:
            self.progressBar = None

    def push(self, x):
        """Method to push onto UI Queue."""
        self.queue.push(x)

    def run(self):
        """Method that runs the main event loop."""
        self.update_ui()
        # run the main event loop of UI
        self.root.mainloop()

    def update_ui(self):
        """Method that updates UI periodically."""
        # update UI with data received
        while self.queue and not self.queue.empty():
            pass
        # update UI after every 200ms
        self.root.after(200, self.update_ui)

    def next_wallpaper(self):
        """Preview next wallpaper."""
        self.index = (self.index + 1) % len(self.images)
        self.gallery.set_image(self.images[self.index])
        self.gallery.slider.set(0)

    def prev_wallpaper(self):
        """Preview previous wallpaper."""
        self.index = (self.index - 1 if self.index != 0
                      else len(self.images) - 1)
        self.gallery.set_image(self.images[self.index])
        self.gallery.slider.set(0)

    def set_wallpaper(self):
        """Set the wallpaper which is being previewed."""
        self.gallery.image.save()
        self.wallpaper.set(self.gallery.image.image_path)

    def flush(self):
        """Method to flush all images."""
        ask = messagebox.askquestion(
                               "Flush!", "Are You Sure? This will empty"
                               " the contents in your pics folder",
                                icon='warning')
        if ask == 'yes':
            flush_wallpapers(self.settings['pics-folder'])
            if active_count() < 2:
                download_thread = Thread(
                                target=download,
                                args=(self.settings['website'],
                                      self.settings['pics-folder'],
                                      self.settings['no-of-images']),
                                daemon=True)
                download_thread.start()
            self.update_images()
        else:
            print("Not Flushing!")

    def update_images(self):
        """Method to get images from directory."""
        print("Updating Image List")
        self.update_pics_from_fav_pics()
        directory = self.settings['pics-folder']
        files = os.listdir(directory)
        self.images = [os.path.join(directory, file) for file in files
                       if (file.endswith('.png') or file.endswith('.jpg'))]

    def update_pics_from_fav_pics(self):
        """Method to inherit the favourite wallpapers back into pics-folder."""
        src_directory = self.settings['fav-pics-folder']
        src_files = os.listdir(src_directory)
        for file_name in src_files:
            full_file_name = os.path.join(src_directory, file_name)
            if (os.path.isfile(full_file_name)):
                copy(full_file_name, self.settings['pics-folder'])

    def play(self):
        """Start scheduling wallpapers."""
        if not self.scheduler_object:
            self.scheduler_object = scheduler(self.settings['offline'],
                                              self.settings['pics-folder'],
                                              self.settings['timeout'],
                                              self.settings['website'],
                                              self.settings['no-of-images'],
                                              not (self.settings['service'] or
                                                   self.settings['ui']),
                                              self.wallpaper)
            self.scheduler_object.setDaemon(True)
            self.scheduler_object.start()

    def favourite(self):
        """Method to copy the favourite image to favourite_pics folder."""
        copy(self.images[self.index], self.settings['fav-pics-folder'])
