"""Module that gets and sets Wallpaper."""

import sys

from subprocess import Popen, PIPE


class Wallpaper:
    """Wallpaper Class that holds set and get functions."""

    def set(self, filename):
        """Set a file as the Wallpaper."""
        if sys.platform.startswith('win32'):  # pragma: no cover
            self.set_wallpaper_windows(filename)

        elif sys.platform.startswith('linux'):
            self.set_wallpaper_linux(filename)

        elif sys.platform.startswith('darwin'):   # pragma: no cover
            self.set_wallpaper_osx(filename)

    def set_wallpaper_linux(self, filename):
        """Set a file as linux Wallpaper."""
        from gi.repository import Gio

        gsettings = Gio.Settings.new('org.gnome.desktop.background')
        gsettings.set_string('picture-uri', "file://" + filename)
        gsettings.apply()

    def set_wallpaper_windows(self, filename):  # pragma: no cover
        """Set a file as windows Wallpaper."""
        import ctypes

        SPI_SETDESKWALLPAPER = 0x14  # which command (20)
        SPIF_UPDATEINIFILE = 0x2  # forces instant update
        ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER,
                                                   0,
                                                   filename,
                                                   SPIF_UPDATEINIFILE)

    def set_wallpaper_osx(self, filename):  # pragma: no cover
        """Set a file as OSX Wallpaper."""
        command = ("osascript -e 'tell application \"System Events\" "
                   "to set picture of every desktop to \"{}\"'"
                   .format(filename))
        process = Popen(command, stdout=PIPE, stderr=PIPE, shell=True)
        _, error = process.communicate()

        if len(error) != 0:
            raise SystemExit(error.decode("utf-8"))

    def get(self):
        """Get file address of current Wallpaper."""
        if sys.platform.startswith('win32'):   # pragma: no cover
            return self.get_wallpaper_windows()

        elif sys.platform.startswith('linux'):
            return self.get_wallpaper_linux()

        elif sys.platform.startswith('darwin'):  # pragma: no cover
            return self.get_wallpaper_osx()

    def get_wallpaper_linux(self):
        """Get current linux Wallpaper."""
        from gi.repository import Gio

        gsettings = Gio.Settings.new('org.gnome.desktop.background')
        return gsettings.get_string('picture-uri')[7:]

    def get_wallpaper_windows(self):  # pragma: no cover
        """Get current windows Wallpaper."""
        import ctypes

        SPI_GETDESKWALLPAPER = 0x73
        path = ctypes.create_unicode_buffer(100)
        ctypes.windll.user32.SystemParametersInfoW(
                                        SPI_GETDESKWALLPAPER,
                                        100, path, 0)
        return path.value

    def get_wallpaper_osx(self):    # pragma: no cover
        """Get current osx Wallpaper."""
        command = ("osascript -e 'tell application \"System Events\" "
                   "to get picture of every desktop'")
        process = Popen(command, stdout=PIPE, stderr=PIPE, shell=True)
        output, error = process.communicate()

        if len(error) != 0:
            raise SystemExit(error.decode("utf-8"))

        return output.decode("utf-8").splitlines()
