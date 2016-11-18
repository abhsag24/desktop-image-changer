from setuptools import setup
import sys

def get_contents(filename):
    file = open(filename, 'r').readlines()
    out = []
    for a in file:
        out.append(a.strip())
    return out

requirements = []
requirements += get_contents('requirements.txt')
if sys.platform.startswith('darwin'):
    requirements += get_contents('mac-requirements.txt')

setup(
    #Name of application:
    name="UIP",

    #Version (initial)
    version="0.1.0",

    #author details:
    author="uip-dev",
    author_email="uip.developers@gmail.com",

    #packages:
    packages=["uiplib"],

    license="LICENSE.txt",

    url="example.com",

    #description
    description="A library to get new wallpapers.",
    long_description=open("README.md").read(),

    #dependencies
    install_requires=requirements,

    #scripts to be run
    scripts=[
        "UIP.py"
    ]
)
