"""The module houses the class that displays wallpapers in the app."""

from tkinter import *
from PIL import ImageTk
from uiplib.uipImage import UipImage


class Gallery(Frame):
    """A view to show the pictures."""

    def __init__(self, master):
        """Initialize the gallery."""
        Frame.__init__(self, master)
        self.image = None
        self.cv = None
        self.label = None
        self.slider = None

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
        self.width = 600
        self.height = 340
        if not self.cv:
            self.cv = Canvas(self, width=self.width, height=self.height)
            self.cv.pack(fill=BOTH, expand=YES)
        if not self.slider:
            self.slider = Scale(self,
                                orient=HORIZONTAL,
                                from_=0, to=30,
                                command=self.blur_image,
                                label="Blur", showvalue=0)
            self.slider.pack()
        self.image = UipImage(imagePath)
        self.show_image(self.image)

    def show_image(self, image):
        """Show the image on canvas."""
        show_image = image.resize((self.width, self.height))
        self.tk_image = ImageTk.PhotoImage(show_image)
        self.cv.create_image(0, 0, anchor="nw", image=self.tk_image)

    def blur_image(self, val):
        """Blur chosen image by val amount."""
        show = self.image.blur(val)
        self.show_image(show)
