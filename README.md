UIP Is Pretty
=============
[![Build Status](https://travis-ci.org/NIT-dgp/UIP.svg?branch=master)](https://travis-ci.org/NIT-dgp/UIP)
[![Build status](https://ci.appveyor.com/api/projects/status/9igx0t9e6e6utt9l/branch/master?svg=true)](https://ci.appveyor.com/project/abhsag24/uip/branch/master)
[![codecov](https://codecov.io/gh/NIT-dgp/UIP/branch/master/graph/badge.svg)](https://codecov.io/gh/NIT-dgp/UIP)

UIP scrapes images from reddit and unsplash, and applies them as a wallpaper
on your desktop(with configurable schedule).
Works with Windows, Mac and Gtk based desktops on Linux.

Examples Of UIP Wallpapers
==========================

![alt text]( https://raw.githubusercontent.com/NIT-dgp/UIP-misc/master/examples/gnome_wallpaper.png )
![alt text]( https://raw.githubusercontent.com/NIT-dgp/UIP-misc/master/examples/mac_wallpaper.png )
![alt text]( https://raw.githubusercontent.com/NIT-dgp/UIP-misc/master/examples/win_wallpaper.png )

Set Up
======

For Users:
----------
To install UIP, just run the command
```
sudo pip install UIP
```

For Testers & Developers:
-------------------------
First clone the source repository from github using the command

```
git clone https://github.com/NIT-dgp/UIP.git
```
To install the requirements run the command

```
sudo python3 setup.py install
```
>Note: We only support Python 3.5 or later versions.

>NOte: make sure you have setuptools, to do that run: pip install setuptools.

>Note: there is no sudo for windows as well as when you have root privelages.
Just run commands without sudo

>Note: some setups use python instead of python3 and pip3 instead of pip

>Note: For some OS' you might need to install Imagetk(needed in our GUI)
seperately for eg: in Ubuntu you can install it by:
`sudo apt-get install python3-pil.imagetk`

Run
===

To run just type

```
UIP
```
from anywhere inside the terminal/console.

If you want to try out our experimental GUI feature:
use: `UIP --ui`

To install requirements for experimental GUI, run:
`pip install -r gui-requirements.txt`

For help use `UIP --help`

Contact Us
==========
https://gitter.im/NIT-dgp/General


How To Package
==============
To package into **source distribution**, run the following command
```
python setup.py sdist
```
**How to test?** (this installs UIP to your library)
```
cd dist/
tar xzf UIP-<version-no>.tar.gz
cd UIP-<version-no>/
python setup.py install
```
How to run?
```
UIP
```

How To Contribute
=================

UIP is in its very early development stage, you can go over the issues on the
github issues page and send in a PR.

your commits in the PR should be of the form:

```
shortlog: commit message

commit body
Fixes <issue number>
```

where short log is the area/filename where you make the change
commit message is the very brief description of the change made by you and any
other additional details go into the commit body.

**Note**: If you're an absolute newcomer, these sources might help you out.
Though keep in mind some of the standards are different.

https://coala.io/newcomer

https://www.atlassian.com/git/tutorials/learn-git-with-bitbucket-cloud

https://try.github.io/levels/1/challenges/1

Testing
=======

While developing, to test, you should first install the test-requirements
by running:

```
pip install -r test-requirements.txt
```
then test your work by the command:
```
pytest
```
If you want to lint your files you can run
```
coala
```
and commit all changes suggested

Do remember to keep your master branch updated at all times
and always work on a different branch.

Happy coding :)
