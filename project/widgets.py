import PyQt5.QtWidgets as qtw
from PyQt5 import QtCore, QtGui
import logging

log = logging.getLogger(__name__)

class Separator(qtw.QFrame):
    """a horizontal separator widget"""
    def __init__(self, orientation:QtCore.Qt.Orientation=QtCore.Qt.Horizontal):
        super().__init__()
        if orientation == QtCore.Qt.Horizontal:
            self.setFrameShape(qtw.QFrame.HLine)
        elif orientation == QtCore.Qt.Vertical:
            self.setFrameShape(qtw.QFrame.VLine)
        else:
            log.error(f"invalid orientation for the separator widget: {orientation} of type {type(orientation)}")
        self.setFrameShadow(qtw.QFrame.Sunken)
