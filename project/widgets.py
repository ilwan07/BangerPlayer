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
    """a widget that displays a square SVG image"""
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

class MusicProgressBar(qtw.QProgressBar):
    """a progress bar that emits a signal with the selected value when clicked and extends when hovered"""
    clickedValue = QtCore.pyqtSignal(float)  # clicked value
    normalSize:int = 8  # normal height of the progress bar
    expandedSize:int = 30  # height of the progress bar when hovered

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setFixedHeight(self.normalSize)

    def mousePressEvent(self, event):
        """emit the clicked value when the progress bar is clicked"""
        if event.button() == QtCore.Qt.LeftButton:
            value = self.minimum() + (self.maximum() - self.minimum()) * event.x() / self.width()
            self.clickedValue.emit(value)
            self.setValue(round(value))
            log.debug(f"clicked on the progress bar at {round(value, 2)}")
        super().mousePressEvent(event)
    
    def enterEvent(self, event):
        """extend the progress bar when hovered"""
        self.setFixedHeight(self.expandedSize)
        super().enterEvent(event)
    
    def leaveEvent(self, event):
        """shrink the progress bar when the mouse leaves"""
        self.setFixedHeight(self.normalSize)
        super().leaveEvent(event)
