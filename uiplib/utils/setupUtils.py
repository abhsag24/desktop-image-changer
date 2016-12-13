import sys
import os


def make_dir(dirpath):
    os.makedirs(dirpath)
    if sys.platform.startswith('linux'):
        os.chmod(dirpath, 0o777)


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
