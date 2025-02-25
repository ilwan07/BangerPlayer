import PyQt5.QtWidgets as qtw
from PyQt5 import QtGui, QtCore
import logging

log = logging.getLogger(__name__)


class Window(qtw.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Banger Player")
        self.show()
