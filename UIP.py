from uiplib.scheduler import scheduler

if __name__ == "__main__":
    print("Hey this is UIP! you can use it to download"
          " images from reddit and also to schedule the setting of these"
          " images as your desktop wallpaper.")
    try:
        print("Press 1 to connect to internet"
              " or any other key to use this"
              " application in offline mode")
        offline = int(input()) != 1
        scheduler(offline)
    except KeyboardInterrupt:
        import sys
        sys.exit(0)
