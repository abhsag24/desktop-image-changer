"""Module that builds the Graphical User Interface."""

import os
from shutil import copy
from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox
from threading import Thread, active_count

from uiplib.gui import generalTab, settingsTab
from uiplib.scheduler import scheduler
from uiplib.utils.utils import flush_wallpapers
from uiplib.settings import DEFAULT_FAVOURITE_PICS_FOLDER
from uiplib.scrape import download
from uiplib.uipImage import UipImage


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
        self.index = 0
        self.images = []
        self.wallpaper = wallpaper
        self.scheduler_object = None

    def create_ui(self):
        """Method to initialize UI."""
        self.notebook = Notebook(self.root)
        self.notebook.pack()
        generalTab.create_general_tab(self)
        settingsTab.create_settings_tab(self)

    def run(self):
        """Method that runs the main event loop."""
        self.create_ui()
        self.update_ui()
        # run the main event loop of UI
        self.root.mainloop()

    def update_ui(self):
        """Method that updates UI periodically."""
        # update UI with data received
        self.update_images()
        self.gallery.update()

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
                                kwargs={'appObj': self},
                                daemon=True)
                download_thread.start()
            self.update_ui()
        else:
            print("Not Flushing!")

    def update_images(self):
        """Method to get images from directory."""
        print("Updating Image List")
        self.update_pics_from_fav_pics()
        directory = self.settings['pics-folder']
        files = os.listdir(directory)
        self.images = [UipImage(os.path.join(directory, file))
                       for file in files if
                       (file.endswith('.png') or file.endswith('.jpg'))]

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
                                              self.wallpaper,
                                              appObj=self)

    def favourite(self):
        """Method to copy the favourite image to favourite_pics folder."""
        if (len(self.images) == 0):
            messagebox.showinfo("Error!",
                                "No images found. Refresh and try again later",
                                icon='warning')
        image_path = self.images[self.index].image_path
        copy(image_path, self.settings['fav-pics-folder'])
        messagebox.showinfo("Success!",
                            "Image successfully saved to favourites")
