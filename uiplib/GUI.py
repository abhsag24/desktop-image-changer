from uiplib.scheduler import scheduler
from uiplib.setWallpaper import change_background
from uiplib.utils import update_settings
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
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

    def create_ui(self):
        ''' Method to initialize UI '''
        self.notebook = Notebook(self.root)
        self.notebook.pack()
        self.create_general_tab()
        self.create_settings_tab()

    def create_settings_tab(self):
        self.new_settings = {}
        settings_tab = Frame(self.notebook)
        self.notebook.add(settings_tab, text="Settings")
        mainFrame = Frame(settings_tab)
        mainFrame.grid(row=0, column=0, sticky=W)

        # Add pics-folder setting
        pics_folder_label = Label(mainFrame, text="Where pics are stored:")
        pics_folder_label.grid(row=0, padx=10, pady=10, sticky=W)
        input_browse = Button(mainFrame,
                              text="Browse",
                              command=self.file_open_helper)
        input_browse.grid(row=0, column=1, padx=10, pady=10, sticky=W)

        # Add sites.
        self.unsplash = BooleanVar()
        self.reddit = BooleanVar()
        self.desktoppr = BooleanVar()
        sites_label = Label(mainFrame, text="Where to download from:")
        sites_label.grid(row=1, padx=10, pady=1, sticky=W)
        sites = ('unsplash', 'reddit', 'desktoppr')
        unsplash_radio = Checkbutton(mainFrame,
                                     text="Unsplash",
                                     var=self.unsplash)
        reddit_radio = Checkbutton(mainFrame,
                                   text="Reddit",
                                   var=self.reddit,
                                   command=lambda: (
                                       self.enable_subreddit(mainFrame)))
        desktoppr_radio = Checkbutton(mainFrame,
                                      text="Desktoppr",
                                      var=self.desktoppr)
        unsplash_radio.grid(row=1, column=1, padx=10, pady=10, sticky=W)
        reddit_radio.grid(row=2, column=1, padx=10, pady=10, sticky=W)
        desktoppr_radio.grid(row=3, column=1, padx=10, pady=10, sticky=W)

        # Timout
        self.timeout_val = StringVar()
        timeout_label = Label(mainFrame, text="Change Wallpaper in:")
        timeout = Entry(mainFrame, textvariable=self.timeout_val)
        timeout_label.grid(row=4, padx=10, pady=10, sticky=W)
        timeout.grid(row=4, column=1, sticky=W)
        minute_label = Label(mainFrame, text="minutes")
        minute_label.grid(row=4, column=2, padx=10, pady=10, sticky=W)

        # Number of images per site
        self.count_val = StringVar()
        count_label = Label(mainFrame, text="No. images per site:")
        count = Entry(mainFrame, textvariable=self.count_val)
        count_label.grid(row=5, padx=10, pady=10, sticky=W)
        count.grid(row=5, column=1, sticky=W)

        # Apply
        apply_button = Button(mainFrame,
                              text="Apply",
                              command=self.handle_settings)
        apply_button.grid(row=6, column=1, pady=20, sticky=W)

    def create_general_tab(self):
        general_width = 1000
        general_height = general_width*3/4
        general = Frame(self.notebook,
                        width=general_width,
                        height=general_height)
        self.notebook.add(general, text="General")
        headerFrame = Frame(general)
        mainFrame = Frame(general)
        footerFrame = Frame(general)

        headerFrame.grid(row=0, column=0, sticky=W+E+N)
        mainFrame.grid(row=1, column=0, sticky=N+E+W+S)
        footerFrame.grid(row=2, column=0, sticky=S+W+E)

        nextButton = Button(mainFrame,
                            text=">",
                            command=self.next_wallpaper)
        prevButton = Button(mainFrame,
                            text="<",
                            command=self.prev_wallpaper)
        nextButton.pack(side=RIGHT, padx=5, pady=5)
        prevButton.pack(side=LEFT, padx=5, pady=5)

        downloadBtn = Button(footerFrame,
                             text="Download",
                             command=self.download)
        setWallpaperBtn = Button(footerFrame,
                                 text="Set Wallpaper",
                                 command=self.set_wallpaper)
        flushBtn = Button(footerFrame,
                          text="Flush",
                          command=self.flush)
        setWallpaperBtn.pack(padx=5, pady=5)
        downloadBtn.pack(padx=5, pady=5)
        flushBtn.pack(padx=5, pady=5)

        self.progress = 0
        self.progressBar = None

        self.gallery = Gallery(mainFrame)
        self.gallery.pack(fill=BOTH)
        if len(self.images) != 0:
            self.gallery.set_image(self.images[self.index])
        else:
            self.gallery.show_error()

    def show_progess(self, show):
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
        image = self.images[self.index]
        change_background(image)

    def enable_subreddit(self, mainFrame):
        sub_label = Label(mainFrame, text="Enter Subreddits")
        sub_label.grid(row=1, column=2, padx=0, pady=0)
        self.sub_entry = Text(mainFrame, height=10, width=20)
        self.sub_entry.grid(row=2, column=2, padx=10, pady=10, sticky=W)

    def download(self):
        pass

    def flush(self):
        print("Flush Clicked!")

    def update_images(self):
        directory = self.settings['pics-folder']
        files = os.listdir(directory)
        self.images = [os.path.join(directory, file) for file in files
                       if (file.endswith('.png') or file.endswith('.jpg'))]

    def file_open_helper(self):
        directory = filedialog.askdirectory()
        self.pics_folder = directory

    def handle_settings(self):
        try:
            self.new_settings['pics-folder'] = self.pics_folder
        except AttributeError as e:
            messagebox.showwarning("AttributeError", "No pics folder selected")
            return
        sites = []
        if self.unsplash.get():
            sites.append("https://unsplash.com/new")
        if self.reddit.get():
            reddit_sites = self.retrieve_textbox_input(self.sub_entry).split()
            sites.extend(reddit_sites)
        if self.desktoppr.get():
            sites.append("https://api.desktoppr.co/1/wallpapers")
        self.new_settings['website'] = sites
        try:
            self.new_settings['timeout'] = int(self.timeout_val.get())*60
        except ValueError:
            messagebox.showwarning("AttributeError",
                                   "Invalid value for timeout")
            return
        try:
            self.new_settings['no-of-images'] = int(self.count_val.get())
        except ValueError:
            messagebox.showwarning("AttributeError",
                                   "Invalid value for no of images")
            return
        update_settings(self.new_settings)

    def retrieve_textbox_input(self, textbox):
        text_input = textbox.get("1.0", END)
        return text_input
