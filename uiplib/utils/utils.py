"""UIP Main utility module."""

import os
import sys
import time
import json
from uiplib.settings import HOME_DIR


def get_percentage(unew, uold, start):
    """Return the percentage of download progress."""
    del_time = (time.time()-float(start))
    if del_time != 0:
        return 100 * ((float(unew) - float(uold)) / del_time)
    return 100


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
