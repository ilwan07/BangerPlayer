from constants import *
import PyQt5.QtWidgets as qtw
from PyQt5 import QtCore, QtGui, QtSvg
from pathlib import Path
import logging
import eyed3
import glob
import vlc

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
        self.svgRender = True
        self.setAlignment(QtCore.Qt.AlignCenter)
        self.setSizePolicy(qtw.QSizePolicy.Expanding, qtw.QSizePolicy.Expanding)
        # We handle painting ourselves, so disable scaledContents.
        self.setScaledContents(False)

    def paintEvent(self, event):
        if self.svgRender:
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
        else:
            super().paintEvent(event)
    
    def setPixmap(self, pixmap:QtGui.QPixmap):
        """if we set a pixmap, switch to the default behavior and deactivate the SVG renderer"""
        super().setPixmap(pixmap)
        self.svgRender = False

class MusicProgressBar(qtw.QProgressBar):
    """a progress bar that emits a signal with the selected value when clicked and extends when hovered"""
    clickedValue = QtCore.pyqtSignal(float)  # clicked value

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.normalSize:int = 8  # normal height of the progress bar
        self.expandedSize:int = 30  # height of the progress bar when hovered
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
    wasRemoved = QtCore.pyqtSignal(Path)  # signal emitted when the folder is deleted

    def __init__(self, folderPath:Path, parent=None):
        super().__init__(parent)
        # some variables
        self.isSelected = False  # track if the folder is selected
        self.dictStyle = {}  # dictionary of styles for the folder widget

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
            if Path(dir).is_file() and Path(dir).suffix in supportedAudioFormats:
                self.nbElements += 1
        self.nbElementsLabel = qtw.QLabel(f"{self.nbElements} Musics")
        self.nbElementsLabel.setFont(Fonts.subtitleFont)
        self.labelsLayout.addWidget(self.nbElementsLabel)

        # remove folder button
        self.removeButton = qtw.QPushButton()
        self.removeButton.setIcon(QtGui.QIcon(str(themeAssetsDir / "icons" / "remove.svg")))
        self.removeButton.setFixedSize(30, 30)
        self.removeButton.setCursor(QtCore.Qt.PointingHandCursor)
        self.removeButton.clicked.connect(lambda: self.wasRemoved.emit(self.folderPath))
        self.mainLayout.addWidget(self.removeButton)

        # mouse tracking
        self.interiorWidgets = (self.iconLabel, self.labelsWidget, self.folderNameLabel, self.nbElementsLabel, self.removeButton)
        self.updateStyle("border-radius", "10px")
        self.updateStyle("border", "2px solid rgba(0, 0, 0, 0)")
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
            self.updateStyle("border", f"2px solid {'white' if colorMode == 'dark' else 'black'}")
            self.isSelected = True
            self.wasSelected.emit(self.folderPath)
        else:
            self.setFrameShape(qtw.QFrame.NoFrame)
            self.updateStyle("border", "2px solid rgba(0, 0, 0, 0)")
            self.isSelected = False

class MusicWidget(qtw.QFrame):
    """a widget that displays a music and its infos in the panel"""
    wasSelected = QtCore.pyqtSignal(Path) # signal emitted when the music is selected

    def __init__(self, musicPath:Path, parent=None):
        super().__init__(parent)
        # some variables
        self.isSelected = False  # track if the music is selected
        self.dictStyle = {}  # dictionary of styles for the music widget

        # main layout
        self.musicPath = musicPath
        self.mainLayout = qtw.QHBoxLayout()
        self.mainLayout.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.setSizePolicy(qtw.QSizePolicy.Expanding, qtw.QSizePolicy.Fixed)
        self.setCursor(QtCore.Qt.PointingHandCursor)
        self.setLayout(self.mainLayout)

        # music cover
        self.coverLabel = SquareVectorLabel(themeAssetsDir / "icons" / "cover.svg")
        self.coverLabel.setFixedSize(100, 100)
        self.mainLayout.addWidget(self.coverLabel)
        
        # music name and author
        self.labelsWidget = qtw.QWidget()
        self.labelsLayout = qtw.QVBoxLayout()
        self.labelsWidget.setLayout(self.labelsLayout)
        self.mainLayout.addWidget(self.labelsWidget)

        # music name
        self.musicNameLabel = qtw.QLabel(musicPath.stem)
        self.musicNameLabel.setFont(Fonts.titleFont)
        self.labelsLayout.addWidget(self.musicNameLabel)

        # music author
        self.authorLabel = qtw.QLabel()
        self.authorLabel.setFont(Fonts.subtitleFont)
        self.labelsLayout.addWidget(self.authorLabel)

        self.mainLayout.addStretch()

        # music length
        self.lengthLabel = qtw.QLabel("[0:00]")
        self.lengthLabel.setFont(Fonts.titleFont)
        self.mainLayout.addWidget(self.lengthLabel)

        self.fetchMetadata()  # fetch the metadata of the music

        # mouse tracking
        self.interiorWidgets = (self.coverLabel, self.labelsWidget, self.musicNameLabel, self.authorLabel, self.lengthLabel)
        self.updateStyle("border-radius", "10px")
        self.updateStyle("border", "2px solid rgba(0, 0, 0, 0)")
        self.setMouseTracking(True)
        self.enterEvent = self.onEnter
        self.leaveEvent = self.onLeave

        self.mousePressEvent = self.onMousePress
    
    def fetchMetadata(self):
        """fetch the metadata of the music and update the widgets accordingly"""
        try:
            # get duration with vlc
            media = vlc.Media(str(self.musicPath))
            media.parse()
            duration = int(media.get_duration() / 1000)
            self.lengthLabel.setText(f"{duration//60}:{duration%60:02}")

            # get metadata with eyed3
            audioFile = eyed3.load(str(self.musicPath))
            if audioFile.tag is None:
                audioFile.initTag()
            if audioFile.tag.title:
                self.musicNameLabel.setText(audioFile.tag.title)
            self.authorLabel.setText(audioFile.tag.artist)
            if audioFile.tag.images:
                # display the cover image
                coverImage = audioFile.tag.images[0]
                coverPixmap = QtGui.QPixmap()
                coverPixmap.loadFromData(coverImage.image_data)
                scaledPixmap = coverPixmap.scaled(self.coverLabel.size(), QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
                self.coverLabel.setPixmap(scaledPixmap)
                
        except Exception as e:
            log.error(f"failed to fetch metadata for {self.musicPath}: {e}")
    
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
            self.updateStyle("border", f"2px solid {'white' if colorMode == 'dark' else 'black'}")
            self.isSelected = True
            self.wasSelected.emit(self.musicPath)
        else:
            self.setFrameShape(qtw.QFrame.NoFrame)
            self.updateStyle("border", "2px solid rgba(0, 0, 0, 0)")
            self.isSelected = False
