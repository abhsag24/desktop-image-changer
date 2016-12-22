import unittest
from uiplib.Wallpaper import Wallpaper
import tempfile
import sys
import pytest


class WallpaperTest(unittest.TestCase):

    @pytest.mark.skipif(not sys.platform.startswith('linux'),
                        reason="test on Linux only")
    def test_wallpaper_linux(self):
        wallpaper = Wallpaper()
        current_wallpaper = wallpaper.get()
        with tempfile.NamedTemporaryFile(mode="wb") as temp_wallpaper:
            wallpaper.set(temp_wallpaper.name)
            self.assertEqual(wallpaper.get(), temp_wallpaper.name)
        wallpaper.set(current_wallpaper)

    @pytest.mark.skipif(not sys.platform.startswith('win32'),
                        reason="test on Windows only")
    def test_wallpaper_windows(self):  # pragma: no cover
        wallpaper = Wallpaper()
        current_wallpaper = wallpaper.get()
        with tempfile.NamedTemporaryFile(mode="wb") as temp_wallpaper:
            wallpaper.set(temp_wallpaper.name)
            self.assertEqual(wallpaper.get(), temp_wallpaper.name)
        wallpaper.set(current_wallpaper)

    @pytest.mark.skipif(not sys.platform.startswith('darwin'),
                        reason="test on OSX only")
    def test_wallpaper_osx(self):   # pragma: no cover
        wallpaper = Wallpaper()
        current_wallpaper = wallpaper.get()[0]
        with tempfile.NamedTemporaryFile(mode="wb") as temp_wallpaper:
            wallpaper.set(temp_wallpaper.name)
            self.assertEqual(
                wallpaper.get()[0], "/private"+temp_wallpaper.name)
        wallpaper.set(current_wallpaper)
