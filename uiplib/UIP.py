import sys, os, shutil
from uiplib.settings import ParseSettings
from uiplib.scheduler import scheduler
if sys.platform.startswith('linux'):
    from uiplib.daemon import daemon

settings = None

class UIP:
    def run(self):
        global settings
        print("Hey this is UIP! you can use it to download"
              " images from reddit and also to schedule the setting of these"
              " images as your desktop wallpaper.")
        try:
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
                      " from reddit.")
            scheduler(settings['offline'],
                      settings['pics-folder'],
                      settings['timeout'],
                      settings['website'][0],
                      settings['no-of-images'])
        except KeyboardInterrupt:
            print("\nExiting UIP hope you had a nice time :)")
            sys.exit(0)

class UIPDaemon(daemon):
    def run(self):
        uip = UIP()
        uip.run()

def main():
    global settings
    settingsParser = ParseSettings()
    settings = settingsParser.settings
    if settings['error']:
        print("\nWRONG USAGE OF FLAGS --no-of-images AND --offline")
        settingsParser.show_help()
        sys.exit(0)
    if settings['service'] and not sys.platform.startswith('win32'):
        daemon = UIPDaemon('/tmp/daemon-uip.pid')
        if 'start' == str(settings['service']):
            daemon.start()
        elif 'stop' == str(settings['service']):
            daemon.stop()
        elif 'restart' == str(settings['service']):
            daemon.restart()
        else:
            print("Unknown command")
            sys.exit(2)
    elif settings['service'] and sys.platform.startswith('win32'):
        print("Sorry, UIP as a service is not yet developed for your OS!")
        sys.exit(1)
    else:
        uip = UIP()
        uip.run()
