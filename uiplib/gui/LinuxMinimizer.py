"""Module that builds the minimized status icon for system tray for Linux."""

from gi.repository import AppIndicator3 as appindicator
from gi.repository import Gtk as gtk
from gi.repository import Notify as notify
from uiplib.gui.mainGui import MainWindow
from uiplib.utils.utils import update_images

APPINDICATOR_ID = 'uip'

#  Notifications

notify_prev = notify.Notification.new(
    "<b>UIP</b>", 'Applying Previous Wallpaper', gtk.STOCK_DIALOG_INFO)
notify_next = notify.Notification.new(
    "<b>UIP</b>", 'Applying Next Wallpaper', gtk.STOCK_DIALOG_INFO)


class LinuxMinimizer:
    """Status Icon Minimizer class."""

    def __init__(self, settings, wallpaper, index, images):
        """Initialize the minimizer."""
        self.wallpaper = wallpaper
        self.settings = settings
        self.index = index
        self.images = images
        self.indicator = appindicator.Indicator.new(
            APPINDICATOR_ID, gtk.STOCK_DIALOG_INFO,
            appindicator.IndicatorCategory.SYSTEM_SERVICES)

    # Menu items

    def quit(self, source):
        """Quit the Minimizer."""
        notify.uninit()
        gtk.main_quit()

    def _prev(self, source):
        """Set Previous wallpaper."""
        notify_prev.show()
        update_images(self)
        self.index = (self.index - 1 if self.index != 0
                      else len(self.images) - 1)
        self.image = self.images[self.index].image_path
        self.set_wallpaper()
        print('Prev image')

    def _next(self, source):
        """Set Next wallpaper."""
        notify_next.show()
        update_images(self)
        self.index = (self.index + 1) % len(self.images)
        self.image = self.images[self.index].image_path
        self.set_wallpaper()
        print('Next image')

    def set_wallpaper(self):
        """Set the wallpaper which is being previewed."""
        self.wallpaper.set(self.image)

    def maximize(self, source):
        """Restore the maximized window of UIP."""
        print('Maximizing UIP')
        app = MainWindow(self.settings, self.wallpaper)
        app.run()

    # Building Menu

    def build_menu(self):
        """Build the menu for status icon."""
        self.menu = gtk.Menu()
        self.item_next = gtk.MenuItem('Next')
        self.item_next.connect('activate', self._next)
        self.menu.append(self.item_next)

        self.item_prev = gtk.MenuItem('Previous')
        self.item_prev.connect('activate', self._prev)
        self.menu.append(self.item_prev)

        self.item_max = gtk.MenuItem('Maximize')
        self.item_max.connect('activate', self.maximize)
        self.menu.append(self.item_max)

        self.item_quit = gtk.MenuItem('Quit')
        self.item_quit.connect('activate', quit)
        self.menu.append(self.item_quit)

        self.menu.show_all()
        return self.menu

    def run(self):
        """Method to run the status icon."""
        self.indicator.set_status(appindicator.IndicatorStatus.ACTIVE)
        self.indicator.set_menu(self.build_menu())
        notify.init(APPINDICATOR_ID)
        gtk.main()
