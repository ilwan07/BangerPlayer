import PyQt5.QtWidgets as qtw
from PyQt5 import QtCore, QtGui
import logging

log = logging.getLogger(__name__)

class Separator(qtw.QWidget):
    """a horizontal separator widget"""
    def __init__(self, orientation:QtCore.Qt.Orientation=QtCore.Qt.Horizontal):
        super().__init__()
        self.widgetLayout = qtw.QHBoxLayout()
        self.setLayout(self.widgetLayout)
        self.frame = qtw.QFrame()
        if orientation == QtCore.Qt.Horizontal:
            self.frame.setFrameShape(qtw.QFrame.HLine)
        elif orientation == QtCore.Qt.Vertical:
            self.frame.setFrameShape(qtw.QFrame.VLine)
        else:
            log.error(f"invalid orientation for the separator widget: {orientation} of type {type(orientation)}")
        self.frame.setFrameShadow(qtw.QFrame.Sunken)
        self.widgetLayout.addWidget(self.frame)
