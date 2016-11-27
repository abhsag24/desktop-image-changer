from uiplib.scheduler import scheduler
from tkinter import *
from tkinter.ttk import *
from PIL import Image, ImageTk
from queue import Queue
import os

class Gallery(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.image = None
        self.cv = None
        self.label = None

    def show_error(self):
        self.image = None
        self.cv = None
        self.label = Label(self, wraplength=150,
                                justify=CENTER,
                                text="No images found. "
                                    "Please refresh and try again!")
        self.label.pack(padx=50, pady=50)


    def set_image(self, imagePath):
        self.label = None
        width = 600
        height = 340
        if not self.cv:
            self.cv = Canvas(self, width=width, height=height)
            self.cv.pack(fill=BOTH, expand=YES)
        self.image = Image.open(imagePath)
        self.image = self.image.resize((width*2, height*2),
                                        Image.ANTIALIAS)
        self.tk_image = ImageTk.PhotoImage(self.image)
        self.cv.create_image(0, 0, image=self.tk_image)

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
        self.index = 0
        self.images = []
        self.update_images()
        # create the UI
        self.create_ui()

    def create_ui(self):
        ''' Method to initialize UI '''
        self.container = Frame(self.root)
        self.container.grid(row=0, column=0)

        self.headerFrame = Frame(self.container)
        self.mainFrame = Frame(self.container)
        self.footerFrame = Frame(self.container)

        self.headerFrame.grid(row=0,column=0, sticky=W+E+N)
        self.mainFrame.grid(row=1,column=0, sticky=N+E+W+S)
        self.footerFrame.grid(row=2,column=0, sticky=S+W+E)

        self.nextButton = Button(self.mainFrame,
                                 text=">",
                                 command=self.next_wallpaper)
        self.prevButton = Button(self.mainFrame,
                                 text="<",
                                 command=self.prev_wallpaper)
        self.nextButton.pack(side=RIGHT, padx=5, pady=5)
        self.prevButton.pack(side=LEFT, padx=5, pady=5)

        self.setWallpaperBtn = Button(self.footerFrame,
                                      text="Set Wallpaper",
                                      command=self.set_wallpaper)
        self.refreshBtn = Button(self.footerFrame,
                                 text="Refresh",
                                 command=self.refresh)
        self.setWallpaperBtn.pack(side=LEFT, padx=5, pady=5)
        self.refreshBtn.pack(side=RIGHT, padx=5, pady=5)

        self.progress = 0
        self.progressBar = None

        self.gallery = Gallery(self.mainFrame)
        self.gallery.pack(fill=BOTH)

        if len(self.images) != 0:
            self.gallery.set_image(self.images[self.index])
        else:
            self.gallery.show_error()


    def show_progess(self, show):
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
        self.update_ui()
        # run the main event loop of UI
        self.root.mainloop()


    def update_ui(self):
        # update UI with data received
        while self.queue and not self.queue.empty():
            pass
        # update UI after every 200ms
        self.root.after(200, self.update_ui)

    def next_wallpaper(self):
        self.index = (self.index + 1) % len(self.images)
        self.gallery.set_image(self.images[self.index])


    def prev_wallpaper(self):
        self.index -= 1
        self.gallery.set_image(self.images[self.index])


    def set_wallpaper(self):
        print("Set wallpaper clicked!")


    def refresh(self):
        print("Refresh Clicked!")

    def update_images(self):
        directory = self.settings['pics-folder']
        files = os.listdir(directory)
        self.images = [os.path.join(directory, file) for file in files
                       if (file.endswith('.png') or file.endswith('.jpg'))]
