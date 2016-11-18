import sys
from scheduler import scheduler

if __name__ == "__main__":
    print("Hey this is UIP! you can use it to download"
          " images from reddit and also to schedule the setting of these"
          " images as your desktop wallpaper.")
    try:
        offline = False
        if len(sys.argv) != 0 and str(sys.argv[1]) == '--offline':
            print("You have choosen to run UIP in offline mode.")
            offline = True
        else:
            print("UIP will now connect to internet and download images"
                  " from reddit.")
        scheduler(offline)
    except KeyboardInterrupt:
        sys.exit(0)
