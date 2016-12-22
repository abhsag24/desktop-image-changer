# Ensure we're in a virtualenv.
if [ "$VIRTUAL_ENV" == "" ]
then
    echo "ERROR: not in a virtual environment."
    exit -1
fi

# Setup variables.
CACHE="/tmp/install-pygtk-$$"

# Make temp directory.
mkdir -p $CACHE

# Test for gobject.
echo -e "\E[1m * Checking for gobject...\E[0m"
python -c "
try: import gobject; raise SystemExit(0)
except ImportError: raise SystemExit(-1)"

if [ $? == 255 ]
then
    echo -e "\E[1m * Installing gobject...\E[0m"
    # Fetch, build, and install gobject.
    (   cd $CACHE
        curl 'http://ftp.acc.umu.se/pub/GNOME/sources/pygobject/3.12/pygobject-3.12.0.tar.xz' > 'pygobject.tar.xz'
        tar -xvf pygobject.tar.xz
        (   cd pygobject*
            ./configure --prefix=$VIRTUAL_ENV PYTHON=python3
            make
            make install
        )
    )
fi
