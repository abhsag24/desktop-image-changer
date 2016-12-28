"""Module to create the General Tab in the GUI."""

from tkinter import *

from uiplib.gui.gallery import Gallery


def create_general_tab(appObj):
    """Method to create general tab."""
    general_width = 1000
    general_height = general_width*3/4
    general = Frame(appObj.notebook,
                    width=general_width,
                    height=general_height)
    appObj.notebook.add(general, text="General")
    headerFrame = Frame(general)
    mainFrame = Frame(general)
    footerFrame = Frame(general)

    headerFrame.grid(row=0, column=0, sticky=W+E+N)
    mainFrame.grid(row=1, column=0, sticky=N+E+W+S)
    footerFrame.grid(row=2, column=0, sticky=S+W+E)

    nextButton = Button(mainFrame,
                        text="▶",
                        command=appObj.next_wallpaper)
    prevButton = Button(mainFrame,
                        text="◀",
                        command=appObj.prev_wallpaper)
    nextButton.pack(side=RIGHT, padx=5, pady=5)
    prevButton.pack(side=LEFT, padx=5, pady=5)

    setWallpaperBtn = Button(footerFrame,
                             text="Set Wallpaper",
                             command=appObj.set_wallpaper)
    flushBtn = Button(footerFrame,
                      text="Flush",
                      command=appObj.flush)
    flushBtn.pack(side=RIGHT, padx=5, pady=5)
    setWallpaperBtn.pack(side=RIGHT, padx=5, pady=5)

    appObj.progress = 0
    appObj.progressBar = None

    appObj.gallery = Gallery(mainFrame)
    appObj.gallery.pack(fill=BOTH)
    if len(appObj.images) != 0:
        appObj.gallery.set_image(appObj.images[appObj.index])
    else:
        appObj.gallery.show_error()
