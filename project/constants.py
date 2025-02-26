from pathlib import Path
from PyQt5 import QtGui
import platformdirs
import darkdetect
import sys

if getattr(sys, "frozen", False):  # if running as a bundled app
    localPath = Path(sys._MEIPASS)
else:  # if running as a script
    localPath = Path(__file__).resolve().parent

appDataDir = Path(platformdirs.user_data_dir("BangerPlayer", appauthor="Ilwan"))  # path to the save data folder
colorMode = "dark" if darkdetect.isDark() else "light"  # color mode of the interface
iconsDir = localPath / "assets" / "icons" / colorMode  # path to the icons directory

class Fonts():
    """a class containing useful fonts"""
    bigTitleFont = QtGui.QFont("Arial", 24)
    titleFont = QtGui.QFont("Arial", 20)
    smallTitleFont = QtGui.QFont("Arial", 18)
    subtitleFont = QtGui.QFont("Arial", 16)
    bigTextFont = QtGui.QFont("Arial", 14)
    textFont = QtGui.QFont("Arial", 11)
