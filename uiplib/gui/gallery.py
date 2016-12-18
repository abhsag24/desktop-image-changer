"""The module houses the class that displays wallpapers in the app."""
from tkinter import *
from PIL import Image, ImageTk


class Gallery(Frame):
    """A view to show the pictures."""

    def __init__(self, master):
        """Initialize the gallery."""
        Frame.__init__(self, master)
        self.image = None
        self.cv = None
        self.label = None

    def show_error(self):
        """Method to display errors."""
        self.image = None
        self.cv = None
        self.label = Label(self, wraplength=150,
                           justify=CENTER,
                           text="No images found. "
                           "Please refresh and try again!")
        self.label.pack(padx=50, pady=50)

    def set_image(self, imagePath):
        """Method to set the image preview."""
        self.label = None
        width = 600
        height = 340
        if not self.cv:
            self.cv = Canvas(self, width=width, height=height)
            self.cv.pack(fill=BOTH, expand=YES)
        self.image = Image.open(imagePath)
        self.image = self.image.resize((width, height),
                                       Image.ANTIALIAS)
        self.tk_image = ImageTk.PhotoImage(self.image)
        self.cv.create_image(0, 0, anchor="nw", image=self.tk_image)
