import sys
import os
import shutil
from uiplib.settings import ParseSettings
from uiplib.scheduler import scheduler
from uiplib.utils import make_dir
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

        elif 'stop' == str(settings['service']):
            try:
                send(pid_file, SIGTERM)
                os.remove(pid_file)
                sys.exit(0)
            except Exception as e:
                print("you need to start a service first", str(e))
                sys.exit(0)
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
            sys.exit(0)
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
            sys.exit(0)
        scheduler(settings['offline'],
                  settings['pics-folder'],
                  settings['timeout'],
                  settings['website'],
                  settings['no-of-images'])
    except KeyboardInterrupt:
        print("Exiting UIP hope you had a nice time :)")
        sys.exit(0)
