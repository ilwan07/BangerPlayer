from constants import *
import PyQt5.QtWidgets as qtw
from PyQt5 import QtCore, QtGui, QtSvg
from pathlib import Path
import logging
import glob

log = logging.getLogger(__name__)

class Separator(qtw.QFrame):
    """a horizontal separator widget"""
    def __init__(self, orientation:QtCore.Qt.Orientation=QtCore.Qt.Horizontal, parent=None):
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
        self.setTextVisible(False)

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

class FolderWidget(qtw.QFrame):
    """a widget that displays a folder and its infos in the panel"""
    wasSelected = QtCore.pyqtSignal(Path) # signal emitted when the folder is selected
    isSelected = False  # track if the folder is selected
    dictStyle = {}  # dictionary of styles for the folder widget

    def __init__(self, folderPath:Path, parent=None):
        super().__init__(parent)

        # main layout
        self.folderPath = folderPath
        self.mainLayout = qtw.QHBoxLayout()
        self.mainLayout.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.setSizePolicy(qtw.QSizePolicy.Expanding, qtw.QSizePolicy.Fixed)
        self.setCursor(QtCore.Qt.PointingHandCursor)
        self.setLayout(self.mainLayout)

        # folder icon
        self.iconLabel = SquareVectorLabel(themeAssetsDir / "icons" / "folder.svg")
        self.iconLabel.setFixedSize(100, 100)
        self.mainLayout.addWidget(self.iconLabel)
        
        # folder infos
        self.labelsWidget = qtw.QWidget()
        self.labelsLayout = qtw.QVBoxLayout()
        self.labelsWidget.setLayout(self.labelsLayout)
        self.mainLayout.addWidget(self.labelsWidget)

        # folder name
        self.folderNameLabel = qtw.QLabel(folderPath.name)
        self.folderNameLabel.setFont(Fonts.titleFont)
        self.labelsLayout.addWidget(self.folderNameLabel)

        # number of music files
        self.nbElements = 0
        for dir in glob.glob(str(folderPath/"*")):
            if Path(dir).is_file() and Path(dir).suffix in [".mp3", ".wav", ".flac", ".ogg", ".m4a"]:
                self.nbElements += 1
        self.nbElementsLabel = qtw.QLabel(f"{self.nbElements} Musics")
        self.nbElementsLabel.setFont(Fonts.subtitleFont)
        self.labelsLayout.addWidget(self.nbElementsLabel)

        # mouse tracking
        self.interiorWidgets = (self.iconLabel, self.labelsWidget, self.folderNameLabel, self.nbElementsLabel)
        self.updateStyle("border-radius", "10px")
        self.setMouseTracking(True)
        self.enterEvent = self.onEnter
        self.leaveEvent = self.onLeave

        self.mousePressEvent = self.onMousePress
    
    def updateStyle(self, key, value):
        """update one specific style element of the folder widget"""
        self.dictStyle[key] = value
        styleString = ""
        for key, value in self.dictStyle.items():
            styleString += f"{key}: {value};"
        self.setStyleSheet(styleString)
        # remove the style for the inner widgets
        for widget in self.interiorWidgets:
            emptyStyleString = ""
            for key in self.dictStyle.keys():
                emptyStyleString += f"{key}: none;"
            widget.setStyleSheet(emptyStyleString)

    def onMousePress(self, event):
        if not self.isSelected:
            self.setSelected(True)
        event.accept()

    def onEnter(self, event):
        self.setHovered(True)
        event.accept()

    def onLeave(self, event):
        self.setHovered(False)
        event.accept()
    
    def setHovered(self, hovered:bool):
        """gray out the frame on hover"""
        if hovered:
            self.updateStyle("background-color", "rgba(0, 0, 0, 64)")
        else:
            self.updateStyle("background-color", "rgba(0, 0, 0, 0)")

    def setSelected(self, selected:bool):
        """outline the frame if selected"""
        if selected:
            self.setFrameShape(qtw.QFrame.Box)
            self.updateStyle("border", "2px solid white")
            self.isSelected = True
            self.wasSelected.emit(self.folderPath)
        else:
            self.setFrameShape(qtw.QFrame.NoFrame)
            self.updateStyle("border", "none")
            self.isSelected = False
