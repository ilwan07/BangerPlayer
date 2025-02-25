from constants import *
import interface
import PyQt5.QtWidgets as qtw
from PyQt5 import QtCore, QtGui
import logging as log
import darkdetect
import ctypes
import sys
import os


log.basicConfig(level=log.DEBUG, filename=appDataDir/"logs"/"latest.log", filemode="w", format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")


if os.name == "nt":  # if on Windows
    appId = "ilwan.bangerplayer"
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(appId)


App = qtw.QApplication(sys.argv)
App.setStyle("Fusion")
App.setApplicationName("BangerPlayer")
if darkdetect.isDark():  # if using dark mode
    # dark mode style found online
    palette = QtGui.QPalette()
    palette.setColor(QtGui.QPalette.Window, QtGui.QColor(53, 53, 53))
    palette.setColor(QtGui.QPalette.WindowText, QtCore.Qt.white)
    palette.setColor(QtGui.QPalette.Base, QtGui.QColor(25, 25, 25))
    palette.setColor(QtGui.QPalette.AlternateBase, QtGui.QColor(53, 53, 53))
    palette.setColor(QtGui.QPalette.ToolTipBase, QtCore.Qt.black)
    palette.setColor(QtGui.QPalette.ToolTipText, QtCore.Qt.white)
    palette.setColor(QtGui.QPalette.Text, QtCore.Qt.white)
    palette.setColor(QtGui.QPalette.Button, QtGui.QColor(53, 53, 53))
    palette.setColor(QtGui.QPalette.ButtonText, QtCore.Qt.white)
    palette.setColor(QtGui.QPalette.BrightText, QtCore.Qt.red)
    palette.setColor(QtGui.QPalette.Link, QtGui.QColor(42, 130, 218))
    palette.setColor(QtGui.QPalette.Highlight, QtGui.QColor(42, 130, 218))
    palette.setColor(QtGui.QPalette.HighlightedText, QtCore.Qt.black)
    App.setPalette(palette)
MainWindow = interface.Window()
sys.exit(App.exec_())
