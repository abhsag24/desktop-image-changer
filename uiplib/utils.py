import os
import sys
import time
import json
from uiplib.settings import HOME_DIR


def get_percentage(unew, uold, start):
    del_time = (time.time()-float(start))
    if del_time != 0:
        return 100 * ((float(unew) - float(uold)) / del_time)
    return 100


def make_dir(dirpath):
    os.makedirs(dirpath)
    if sys.platform.startswith('linux'):
        os.chmod(dirpath, 0o777)


def update_settings(new_settings):
    settings_file = os.path.join(HOME_DIR, 'settings.json')
    temp_file = os.path.join(HOME_DIR, 'temp.json')
    with open(temp_file, "w+") as _file:
        _file.write(json.dumps(new_settings, indent=4, sort_keys=True))
    os.remove(settings_file)
    os.rename(temp_file, settings_file)


def check_version():
    """Check for the version of python interpreter"""
    # Required version of python interpreter
    req_version = (3, 5)
    # Current version of python interpreter
    curr_version = sys.version_info

    # Exit if minimum requirements are not met
    if curr_version < req_version:
        raise SystemExit("Your python interpreter does not meet" +
                         " the minimum requirements.\n" +
                         "Consider upgrading to python3.5")
