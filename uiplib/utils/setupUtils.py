"""Utility module for setup."""

import sys
import os


def make_dir(dirpath):
    """Create a directory for the specified path."""
    os.makedirs(dirpath)
    if sys.platform.startswith('linux'):
        os.chmod(dirpath, 0o777)


def get_current_version():
    """Retrieve the current python interpreter version."""
    return sys.version_info


def check_version():
    """Check the version of python interpreter."""
    # Required version of python interpreter
    req_version = (3, 5)
    # Current version of python interpreter
    curr_version = get_current_version()

    # Exit if minimum requirements are not met
    if curr_version < req_version:
        raise SystemExit("Your python interpreter does not meet" +
                         " the minimum requirements.\n" +
                         "Consider upgrading to python3.5")
