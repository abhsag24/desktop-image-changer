import sys, os, shutil
from uiplib.settings import ParseSettings
from uiplib.scheduler import scheduler

def main():
    print("Hey this is UIP! you can use it to download"
          " images from reddit and also to schedule the setting of these"
          " images as your desktop wallpaper."
          " \nPress ctrl-c to exit")

    settingsParser = ParseSettings()
    settings = settingsParser.settings
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
                os.mkdir(settings['pics-folder'])
            except FileNotFoundError:
                pass
        if not settings['offline']:
            print("UIP will now connect to internet and download images"
                  " from reddit and unsplash.")
        scheduler(settings['offline'],
                  settings['pics-folder'],
                  settings['timeout'],
                  settings['website'],
                  settings['no-of-images'])
    except KeyboardInterrupt:
        print("Exiting UIP hope you had a nice time :)")
        sys.exit(0)
