"""Module to create a settings tab in the GUI."""

from tkinter import *
from tkinter import filedialog
from tkinter import messagebox

from uiplib.settings import DEFAULT_SETTINGS
from uiplib.utils.utils import check_sites, update_settings


def create_settings_tab(appObj):
    """Method to create settings tab."""
    appObj.new_settings = {}
    settings_tab = Frame(appObj.notebook)
    appObj.notebook.add(settings_tab, text="Settings")
    mainFrame = Frame(settings_tab)
    mainFrame.grid(row=0, column=0, sticky=W)

    # Add pics-folder setting
    pics_folder_label = Label(mainFrame, text="Where pics are stored:")
    pics_folder_label.grid(row=0, padx=10, pady=10, sticky=W)
    appObj.pics_folder = StringVar()
    input_browse = Button(mainFrame,
                          text="Browse",
                          command=lambda: file_open_helper(appObj,
                                                           appObj.pics_folder))
    input_browse.grid(row=0, column=1, padx=10, pady=10, sticky=W)
    appObj.pics_folder.set(appObj.settings['pics-folder'])
    choice_label = Label(mainFrame, textvariable=appObj.pics_folder)
    choice_label.grid(row=0, column=2,
                      padx=10, pady=10,
                      sticky=W)

    # Add fav-pics-folder setting
    fav_pics_folder_label = Label(mainFrame, text="Where fav-pics are stored:")
    fav_pics_folder_label.grid(row=1, padx=10, pady=10, sticky=W)
    appObj.fav_pics_folder = StringVar()
    input_browse1 = Button(mainFrame,
                           text="Browse",
                           command=lambda: (
                               file_open_helper(appObj,
                                                appObj.fav_pics_folder)))
    input_browse1.grid(row=1, column=1, padx=10, pady=10, sticky=W)
    appObj.fav_pics_folder.set(appObj.settings['fav-pics-folder'])
    choice_label1 = Label(mainFrame, textvariable=appObj.fav_pics_folder)
    choice_label1.grid(row=1, column=2,
                       padx=10, pady=10,
                       sticky=W)

    # Add sites.
    appObj.unsplash = BooleanVar()
    appObj.reddit = BooleanVar()
    appObj.desktoppr = BooleanVar()
    appObj.sites_list = check_sites(appObj.settings)
    appObj.unsplash.set(appObj.sites_list['unsplash'])
    appObj.desktoppr.set(appObj.sites_list['desktoppr'])
    if appObj.sites_list['reddit']:
        appObj.reddit.set(True)
        toggle_subreddit(appObj, mainFrame)
    else:
        appObj.reddit.set(False)
    sites_label = Label(mainFrame, text="Where to download from:")
    sites_label.grid(row=2, padx=10, pady=1, sticky=W)
    unsplash_radio = Checkbutton(mainFrame,
                                 text="Unsplash",
                                 var=appObj.unsplash)
    reddit_radio = Checkbutton(mainFrame,
                               text="Reddit",
                               var=appObj.reddit,
                               command=lambda: (
                                   toggle_subreddit(appObj, mainFrame)))
    desktoppr_radio = Checkbutton(mainFrame,
                                  text="Desktoppr",
                                  var=appObj.desktoppr)
    unsplash_radio.grid(row=2, column=1, padx=10, pady=10, sticky=W)
    reddit_radio.grid(row=3, column=1, padx=10, pady=10, sticky=W)
    desktoppr_radio.grid(row=4, column=1, padx=10, pady=10, sticky=W)

    # Timout
    appObj.timeout_val = StringVar()
    appObj.timeout_val.set(int(int(appObj.settings['timeout'])/60))
    timeout_label = Label(mainFrame, text="Change Wallpaper in:")
    timeout = Entry(mainFrame, textvariable=appObj.timeout_val)
    timeout_label.grid(row=5, padx=10, pady=10, sticky=W)
    timeout.grid(row=5, column=1, sticky=W)
    minute_label = Label(mainFrame, text="minutes")
    minute_label.grid(row=5, column=2, padx=10, pady=10, sticky=W)

    # Number of images per site
    appObj.count_val = StringVar()
    appObj.count_val.set(appObj.settings["no-of-images"])
    count_label = Label(mainFrame, text="No. images per site:")
    count = Entry(mainFrame, textvariable=appObj.count_val)
    count_label.grid(row=6, padx=10, pady=10, sticky=W)
    count.grid(row=6, column=1, sticky=W)

    # Number to days to auto-delete
    appObj.auto_del_val = StringVar()
    val = int(appObj.settings['days-to-autodel']/(24*60*60))
    appObj.auto_del_val.set(val)
    auto_del_label = Label(mainFrame, text="Auto-delete Wallpaper in:")
    autodel = Entry(mainFrame, textvariable=appObj.auto_del_val)
    auto_del_label.grid(row=7, padx=10, pady=10, sticky=W)
    autodel.grid(row=7, column=1, sticky=W)
    days_label = Label(mainFrame, text="days")
    days_label.grid(row=7, column=2, padx=10, pady=10, sticky=W)

    # Apply
    apply_button = Button(mainFrame,
                          text="Apply",
                          command=lambda: handle_settings(appObj))
    apply_button.grid(row=8, column=1, pady=10, sticky=W)

    # Reset
    default_button = Button(mainFrame,
                            text="Reset",
                            command=lambda: (
                                update_settings_view(appObj,
                                                     mainFrame,
                                                     DEFAULT_SETTINGS)))
    default_button.grid(row=8, column=2, pady=10, sticky=W)


def toggle_subreddit(appObj, mainFrame):
    """Method to toggle the subreddit choice pane."""
    if appObj.reddit.get():
        try:
            appObj.sub_label.grid()
            appObj.sub_entry.grid()
        except AttributeError:
            appObj.sub_label = Label(mainFrame, text="Enter Subreddits")
            appObj.sub_entry = Text(mainFrame, height=10, width=20)
            for subreddit in appObj.sites_list['reddit']:
                appObj.sub_entry.insert(INSERT, subreddit + " \n")
            appObj.sub_label.grid(row=2, column=2, padx=0, pady=0)
            appObj.sub_entry.grid(row=3, column=2, padx=10, pady=10, sticky=W)
    else:
        appObj.sub_label.grid_remove()
        appObj.sub_entry.grid_remove()


def file_open_helper(appObj, folder):
    """Open the dialog to choose folder."""
    directory = filedialog.askdirectory()
    folder.set(directory)
    appObj.root.update_idletasks()


def handle_settings(appObj):
    """Handler to update the settings file."""
    try:
        appObj.new_settings['pics-folder'] = appObj.pics_folder.get()
        appObj.new_settings['fav-pics-folder'] = appObj.fav_pics_folder.get()
    except AttributeError:
        messagebox.showwarning("AttributeError", "Folder not selected")
        return
    sites = []
    if appObj.unsplash.get():
        sites.append("https://unsplash.com/new")
    if appObj.reddit.get():
        reddit_sites = retrieve_textbox_input(appObj, appObj.sub_entry).split()
        sites.extend(reddit_sites)
    if appObj.desktoppr.get():
        sites.append("https://api.desktoppr.co/1/wallpapers")
    appObj.new_settings['website'] = sites
    try:
        appObj.new_settings['timeout'] = int(appObj.timeout_val.get())*60
    except ValueError:
        messagebox.showwarning("AttributeError",
                               "Invalid value for timeout")
        return
    try:
        appObj.new_settings['no-of-images'] = int(appObj.count_val.get())
    except ValueError:
        messagebox.showwarning("AttributeError",
                               "Invalid value for no of images")
        return
    try:
        val = int(appObj.auto_del_val.get())
        appObj.new_settings['days-to-autodel'] = val*24*60*60
    except ValueError:
        messagebox.showwarning("AttributeError",
                               "Invalid value for no of days to auto-delete")
        return
    update_settings(appObj.new_settings)


def update_settings_view(appObj, mainFrame, settings):
    """Update and view default settings when Reset is pressed."""
    appObj.pics_folder.set(settings['pics-folder'])
    appObj.fav_pics_folder.set(settings['fav-pics-folder'])
    appObj.sites_list = check_sites(settings)
    appObj.unsplash.set(appObj.sites_list['unsplash'])
    appObj.desktoppr.set(appObj.sites_list['desktoppr'])
    if appObj.sites_list['reddit']:
        appObj.reddit.set(True)
        toggle_subreddit(appObj, mainFrame)
    else:
        appObj.reddit.set(False)
        toggle_subreddit(appObj, mainFrame)
    appObj.timeout_val.set(int(int(settings['timeout'])/60))
    appObj.count_val.set(settings["no-of-images"])
    appObj.auto_del_val.set(int(settings["days-to-autodel"]/(24*60*60)))
    appObj.root.update_idletasks()
    update_settings(settings)


def retrieve_textbox_input(appObj, textbox):
    """Handler to fetch the textbox input."""
    text_input = textbox.get("1.0", END)
    return text_input
