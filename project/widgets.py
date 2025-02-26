import PyQt5.QtWidgets as qtw
from PyQt5 import QtCore, QtGui, QtSvg
from pathlib import Path
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

class SquareVectorLabel(qtw.QLabel):
    def __init__(self, svgPath:Path, parent=None):
        super().__init__(parent)
        self.svg_renderer = QtSvg.QSvgRenderer(str(svgPath))
        self.setAlignment(QtCore.Qt.AlignCenter)
        self.setSizePolicy(qtw.QSizePolicy.Expanding, qtw.QSizePolicy.Expanding)
        # We handle painting ourselves, so disable scaledContents.
        self.setScaledContents(False)

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        rect = self.rect()
        # Determine the largest square that fits inside the widget.
        side = min(rect.width(), rect.height())
        square_rect = QtCore.QRect(
            (rect.width() - side) // 2,
            (rect.height() - side) // 2,
            side,
            side,
        )
        painter.save()
        # Optionally enable antialiasing for smoother rendering.
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        # Clip drawing to the square area.
        painter.setClipRect(square_rect)
        # Move the painter’s origin to the top-left of the square.
        painter.translate(square_rect.topLeft())
        # Render the SVG to fill the square area.
        self.svg_renderer.render(painter, QtCore.QRectF(0, 0, side, side))
        painter.restore()
