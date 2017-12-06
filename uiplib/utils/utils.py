"""UIP Main utility module."""

import os
import time
import json
import shutil
import sys

from uiplib.settings import HOME_DIR
from uiplib.utils.setupUtils import make_dir
from uiplib.uipImage import UipImage


def get_percentage(unew, uold, start):
    """Return the percentage of download progress."""
    del_time = (time.time()-float(start))
    if del_time != 0:
        return 100 * ((float(unew) - float(uold)) / del_time)
    return 100  # pragma: no cover
    # This is highly unlikely for time.time() - time.time() to be 0
    # atleast as close to 0.0001 difference exists


def update_settings(new_settings):  # pragma: no cover
    """Update the settings file with the new settings."""
    settings_file = os.path.join(HOME_DIR, 'settings.json')
    temp_file = os.path.join(HOME_DIR, 'temp.json')
    with open(temp_file, "w+") as _file:
        _file.write(json.dumps(new_settings, indent=4, sort_keys=True))
    os.remove(settings_file)
    os.rename(temp_file, settings_file)


def check_sites(settings):
    """Check the presence of sites and update settings as necessary."""
    sites_present = {
        'unsplash': False,
        'reddit': [],
        'desktoppr': False
    }
    for site in settings['website']:
        for key in sites_present:
            if key in site:
                if key == 'reddit':
                    sites_present[key].append(site)
                else:
                    sites_present[key] = True
    return sites_present


def flush_wallpapers(folder):
    """Delete all downloaded wallpapers."""
    print("Deleting all downloaded wallpapers...")
    try:
        shutil.rmtree(folder)
        make_dir(folder)
    except FileNotFoundError:
        pass


def exit_UIP():  # pragma: no cover
    """Exit from UIP program."""
    print("\nExiting UIP hope you had a nice time :)")
    sys.exit(0)


def auto_flush(settings):
    """Automatically deletes old wallpapers."""
    images = os.listdir(settings['pics-folder'])
    for image in images:
        image_path = os.path.join(settings['pics-folder'], image)
        delta = time.time() - os.path.getmtime(image_path)
        if delta > settings['days-to-autodel']:
            os.remove(image_path)
