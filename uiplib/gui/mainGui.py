"""Module that builds the Graphical User Interface."""

from uiplib.scheduler import scheduler
from uiplib.utils.utils import update_settings, check_sites
from uiplib.gui.gallery import Gallery
from uiplib.gui import generalTab, settingsTab


from tkinter import *
from tkinter import messagebox
from tkinter.ttk import *
from PIL import Image, ImageTk
from queue import Queue
import os


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

    def prev_wallpaper(self):
        """Preview previous wallpaper."""
        self.index = (self.index - 1 if self.index != 0
                      else len(self.images) - 1)
        self.gallery.set_image(self.images[self.index])

    def set_wallpaper(self):
        """Set the wallpaper which is being previewed."""
        image = self.images[self.index]
        self.wallpaper.set(image)

    def download(self):
        """Method to start download."""
        pass

    def flush(self):
        """Method to flush all images."""
        print("Flush Clicked!")

    def update_images(self):
        """Method to get images from directory."""
        directory = self.settings['pics-folder']
        files = os.listdir(directory)
        self.images = [os.path.join(directory, file) for file in files
                       if (file.endswith('.png') or file.endswith('.jpg'))]
