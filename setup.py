"""Module to perform build, package and install."""

import os
import json

from uiplib.utils.setupUtils import check_version, make_dir
check_version()
# Proceed only if the version is greater else exits

from setuptools import setup
from uiplib.settings import (HOME_DIR,
                             DEFAULT_PICS_FOLDER,
                             NUMBER_OF_IMAGES_TO_PARSE,
                             DEFAULT_FAVOURITE_PICS_FOLDER,
                             settings_file_path,
                             DEFAULT_SETTINGS)


def get_packages():
    """Method to retrieve packages to be bundled."""
    base_dir = 'uiplib'
    packages = [base_dir]
    for (path, dirs, files) in os.walk(base_dir):
        try:
            dirs.remove('__pycache__')
        except ValueError:
            pass
        if '__init__.py' in files:
            packages.extend([os.path.join(path, dir) for dir in dirs])
    return packages


def get_requirements(filename):
    """Method to get the requirements of the specified file."""
    file = open(filename, 'r').readlines()
    out = []
    for a in file:
        out.append(a.strip())
    return out


# Make Home Directory
if not os.path.exists(HOME_DIR):
    make_dir(HOME_DIR)

if not os.path.exists(DEFAULT_PICS_FOLDER):
    make_dir(DEFAULT_PICS_FOLDER)

if not os.path.exists(DEFAULT_FAVOURITE_PICS_FOLDER):
    make_dir(DEFAULT_FAVOURITE_PICS_FOLDER)

if not os.path.isfile(settings_file_path):
    file_data = DEFAULT_SETTINGS

    with open(settings_file_path, "w") as settings_file:
        settings_file.write(json.dumps(file_data, indent=4, sort_keys=True))

requirements = get_requirements('requirements.txt')

setup(
    # Name of application:
    name="UIP",

    version="0.0.3",

    # author details:
    author="uip-dev",
    author_email="uip.developers@gmail.com",

    # packages:
    packages=get_packages(),

    license="LICENSE",

    url="https://www.github.com/NIT-dgp/UIP",

    # description
    description="A library to get new wallpapers.",
    long_description=open("README.md").read(),

    # dependencies
    install_requires=requirements,

    # scripts to be run
    scripts=[
        "UIP"
    ],

    # binaries that can be called from anywhere
    entry_points={
        "console_scripts": [
                  "UIP = uiplib.UIP:main"]}


)
