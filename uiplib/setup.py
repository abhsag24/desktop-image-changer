import sys
import os
import json

from uiplib.utils import check_version, make_dir
check_version()

from uiplib.settings import (HOME_DIR,
                             DEFAULT_PICS_FOLDER,
                             NUMBER_OF_IMAGES_TO_PARSE,
                             settings_file_path)
def makeHomeDirs():
    # Make Home Directory
    if not os.path.exists(HOME_DIR):
        make_dir(HOME_DIR)
    
    if not os.path.exists(DEFAULT_PICS_FOLDER):
        make_dir(DEFAULT_PICS_FOLDER)
    
    if not os.path.isfile(settings_file_path):
        file_data = {'timeout': 30*60,
                    'no-of-images': NUMBER_OF_IMAGES_TO_PARSE,
                    'pics-folder': DEFAULT_PICS_FOLDER,
                    'website': ['https://unsplash.com/new',
                                'https://www.reddit.com/r/wallpapers/',
                                'https://www.reddit.com/r/wallpaper/',
                                'https://www.reddit.com/r/EarthPorn/',
                                'https://www.reddit.com/r/VillagePorn/',
                                'https://www.reddit.com/r/pics/']}
        with open(settings_file_path, "w") as settings_file:
            settings_file.write(json.dumps(file_data))
