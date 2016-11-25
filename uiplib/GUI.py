from uiplib.scheduler import scheduler
from tkinter import *
from tkinter.ttk import *
from PIL import Image, ImageTk
from queue import Queue
import os
import time # remove this later on

class Gallery(Frame):
    def __init__(self, master, imagePath):
        Frame.__init__(self, master)
        self.width = 400
        self.height = 300
        if not imagePath:
            self.showError()
        else:
            self.setup(imagePath)


    def showError(self):
        self.label = Label(self, wraplength=150,
                                 justify=CENTER,
                                 text="No images found. "
                                      "Please refresh and try again!")
        self.label.pack(padx=50, pady=50)


    def setup(self, imagePath):
        self.cv = Canvas(self, width=self.width, height=self.height)
        self.cv.pack(fill=BOTH, expand=YES)
        self.image = Image.open(imagePath)
        self.image = self.image.resize((self.width, self.height),
                                        Image.ANTIALIAS)
        self.tk_image = ImageTk.PhotoImage(self.image)
        cv.create_image(0, 0, image=self.tk_image)

class MainWindow:
    ''' The main window that houses the app '''
    def __init__(self, settings):
        # configuration
        self.settings = settings
        # base window
        self.root = Tk()
        # set window title
        self.root.title("UIP")
        # self.root.wm_iconbitmap() sets icon bitmap
        self.queue = Queue()
        # create the UI
        self.createUI()
        self.index = 0


    def createUI(self):
        ''' Method to initialize UI '''
        self.container = Frame(self.root)
        self.container.grid(row=0, column=0)

        self.headerFrame = Frame(self.container)
        self.mainFrame = Frame(self.container)
        self.footerFrame = Frame(self.container)

        self.headerFrame.grid(row=0,column=0, sticky=W+E+N)
        self.mainFrame.grid(row=1,column=0, sticky=N+E+W+S)
        self.footerFrame.grid(row=2,column=0, sticky=S+W+E)

        self.nextButton = Button(self.mainFrame, text=">")
        self.prevButton = Button(self.mainFrame, text="<")
        self.nextButton.pack(side=RIGHT, padx=5, pady=5)
        self.prevButton.pack(side=LEFT, padx=5, pady=5)

        self.setWallpaperBtn = Button(self.footerFrame,
                                      text="Set Wallpaper",
                                      command=self.setWallpaper)
        self.refreshBtn = Button(self.footerFrame,
                                 text="Refresh",
                                 command=self.refresh)
        self.setWallpaperBtn.pack(side=LEFT, padx=5, pady=5)
        self.refreshBtn.pack(side=RIGHT, padx=5, pady=5)

        self.progress = 0
        self.progressBar = None

        self.gallery = Gallery(self.mainFrame, None)
        self.gallery.pack(fill=BOTH)


    def showProgess(self, show):
        if show:
            self.progressBar = Progressbar(self.headerFrame,
                                        orient = HORIZONTAL,
                                        length = '300',
                                        variable = self.progress,
                                        mode='determinate')
            self.progressBar.pack(fill=BOTH, padx=5, pady=5)
        else:
            self.progressBar = None


    def push(self, x):
        self.queue.push(x)


    def run(self):
        self.updateUI()
        # run the main event loop of UI
        self.root.mainloop()


    def updateUI(self):
        # update UI with data received
        while self.queue and not self.queue.empty():
            pass
        print(time.ctime()) #remove this comment
        # update UI after every 200ms
        self.root.after(200, self.updateUI)


    def setWallpaper(self):
        print("Set wallpaper clicked!")


    def refresh(self):
        print("Refresh Clicked!")
