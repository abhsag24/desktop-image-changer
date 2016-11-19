import sys, argparse, os, shutil
from uiplib.constants import CURR_DIR, PICS_FOLDER
from uiplib.scheduler import scheduler

if __name__ == "__main__":
    print("Hey this is UIP! you can use it to download"
          " images from reddit and also to schedule the setting of these"
          " images as your desktop wallpaper.")
    parser = argparse.ArgumentParser()
    parser.add_argument("--offline", action="store_true",
                        help="Runs UIP in offline mode.")
    parser.add_argument("--flush", action="store_true",
                        help="Delete all downloaded wallpapers"
                             " and downloads new ones. "
                             "When combined with --offline,"
                             " deletes the wallpapers and exits.")
    args = parser.parse_args()
    try:
        if args.offline:
            print("You have choosen to run UIP in offline mode.")
        if args.flush:
            print("Deleting all downloaded wallpapers...")
            try:
                shutil.rmtree(os.path.join(CURR_DIR, PICS_FOLDER))
                os.mkdir(os.path.join(CURR_DIR, PICS_FOLDER))
            except FileNotFoundError:
                pass
        if not args.offline:
            print("UIP will now connect to internet and download images"
                  " from reddit.")
        scheduler(args.offline)
    except KeyboardInterrupt:
        sys.exit(0)
