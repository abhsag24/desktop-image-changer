import sys
import os
import shutil
from uiplib.settings import ParseSettings, HOME_DIR
from uiplib.scheduler import scheduler
from uiplib.utils import make_dir, exit_UIP
from daemoniker import Daemonizer, send, SIGTERM


def main():
    settingsParser = ParseSettings()
    settings = settingsParser.settings
    pid_file = os.path.join(HOME_DIR, 'daemon-uip.pid')
    if settings['service']:
        if 'start' == str(settings['service']):
            with Daemonizer() as (is_setup, daemonizer):
                if is_setup:
                    print("UIP will now run as a serice.")
                try:
                    is_parent = daemonizer(pid_file)
                except SystemExit:
                    print("UIP service already, running "
                          "Close previous app by running UIP --service stop")
                    sys.exit(0)

        elif 'stop' == str(settings['service']):
            exit_UIP()
        else:
            print('Wrong option for service flag see --help')

    print("Hey this is UIP! you can use it to download"
          " images from reddit and also to schedule the setting of these"
          " images as your desktop wallpaper."
          " \nPress ctrl-c to exit")
    try:
        if settings['error']:
            print("\nWRONG USAGE OF FLAGS --no-of-images AND --offline")
            settingsParser.show_help()
            exit_UIP()
        if settings['offline']:
            print("You have choosen to run UIP in offline mode.")
        if settings['flush']:
            print("Deleting all downloaded wallpapers...")
            try:
                shutil.rmtree(settings['pics-folder'])
                make_dir(settings['pics-folder'])
            except FileNotFoundError:
                pass
        if not settings['offline']:
            print("UIP will now connect to internet and download images"
                  " from reddit and unsplash.")
        if settings['ui']:
            from uiplib.GUI import MainWindow
            app = MainWindow(settings)
            app.run()
            exit_UIP()
        scheduler(settings['offline'],
                  settings['pics-folder'],
                  settings['timeout'],
                  settings['website'],
                  settings['no-of-images'])
    except KeyboardInterrupt:
        exit_UIP()
