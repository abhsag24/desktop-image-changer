"""A class that handles editing of images before applying as wallpaper."""

import os

from PIL import Image, ImageFilter


class UipImage:
    """Class that holds the image as well as the functions used to edit it."""

    def __init__(self, image_path):
        """Initialize class."""
        self.image_path = image_path
        self.original_path = image_path
        self.image = Image.open(image_path)
        self.edited = False
        self._blur = False
        self.blur_radius = 0

    def blur(self, radius):
        """Save blur pamaters as well as returns a blurred image."""
        self.edited = True
        self._blur = True
        self._blur_radius = radius
        return self.image.filter(ImageFilter.GaussianBlur(
                                      radius=float(radius)))

    def save(self):
        """Save the image while applying all the parameters used to edit it."""
        if self.edited:
            filename, ext = os.path.splitext(self.original_path)
            self.image_path = os.path.join(filename + '_uip' + ext)
            if self._blur:
                self.image = self.blur(self._blur_radius)
        self.image.save(self.image_path)
