import sys


def change_background(filename):
    if sys.platform.startswith('win32'):
        change_windows_background(filename)

    elif sys.platform.startswith('linux'):
        change_linux_background(filename)

    elif sys.platform.startswith('darwin'):
        change_osx_background(filename)


def change_linux_background(filename):
    from gi.repository import Gio

    gsettings = Gio.Settings.new('org.gnome.desktop.background')
    gsettings.set_string('picture-uri', "file://" + filename)
    gsettings.apply()


def change_windows_background(filename):
    import ctypes

    SPI_SETDESKWALLPAPER = 0x14  # which command (20)
    SPIF_UPDATEINIFILE = 0x2  # forces instant update
    print(ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER,
                                                     0,
                                                     filename,
                                                     SPIF_UPDATEINIFILE))


def change_osx_background(filename):
    from appscript import app, mactypes  # use applescript modules

    se = app('System Events')  # fetch system events
    desktops = se.desktops.display_name.get()  # get all available displays
    for d in desktops:
        desk = se.desktops[d]
        # set wallpaper for each display
        desk.picture.set(mactypes.File(filename))
