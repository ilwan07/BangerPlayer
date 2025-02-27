from constants import *
from widgets import *
import PyQt5.QtWidgets as qtw
from PyQt5 import QtCore, QtGui
import darkdetect
import logging

log = logging.getLogger(__name__)


class Window(qtw.QMainWindow):
    """main window class for the BangerPlayer application"""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Banger Player")
        self.setWindowIcon(QtGui.QIcon(str(themeAssetsDir / "logo" / "logo.svg")))
        log.debug("window instance created")
    
    def startInterface(self):
        """start the main interface"""
        log.info("starting the main interface")
        self.buildMainInterface()
        self.buildFoldersPanel()
        self.buildMusicsPanel()
        self.buildPlayerPanel()
        self.setupInterface()
        log.info("interface loaded, now showing the window")
        self.showMaximized()
        self.show()
    
    def buildMainInterface(self):
        """build the main interface"""
        # create the main widget
        self.centralWidget = qtw.QWidget()
        self.setCentralWidget(self.centralWidget)
        self.mainLayout = qtw.QHBoxLayout()
        self.centralWidget.setLayout(self.mainLayout)
        log.debug("created main widget and layout")

        # create the main panels
        self.foldersPanel = qtw.QWidget()
        self.musicsPanel = qtw.QWidget()
        self.playerPanel = qtw.QWidget()

        self.foldersPanelLayout = qtw.QVBoxLayout()
        self.musicsPanelLayout = qtw.QVBoxLayout()
        self.playerPanelLayout = qtw.QVBoxLayout()

        self.foldersPanelLayout.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignTop)
        self.musicsPanelLayout.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignTop)
        self.playerPanelLayout.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignTop)

        self.foldersPanel.setSizePolicy(qtw.QSizePolicy.Expanding, qtw.QSizePolicy.Expanding)
        self.musicsPanel.setSizePolicy(qtw.QSizePolicy.Expanding, qtw.QSizePolicy.Expanding)
        self.playerPanel.setSizePolicy(qtw.QSizePolicy.Expanding, qtw.QSizePolicy.Expanding)

        self.foldersPanel.setLayout(self.foldersPanelLayout)
        self.musicsPanel.setLayout(self.musicsPanelLayout)
        self.playerPanel.setLayout(self.playerPanelLayout)
        log.debug("instanciated main panels")

        # create the splitter
        self.mainSplitter = qtw.QSplitter(QtCore.Qt.Horizontal)
        self.mainLayout.addWidget(self.mainSplitter)
        self.mainSplitter.addWidget(self.foldersPanel)
        self.mainSplitter.addWidget(self.musicsPanel)
        self.mainSplitter.addWidget(self.playerPanel)
        self.mainSplitter.setSizes([400, 400, 400])

        # Add a line to make the splitter visible
        for i in range(self.mainSplitter.count()):
            handle = self.mainSplitter.handle(i)
            line = qtw.QFrame(handle)
            line.setFrameShape(qtw.QFrame.VLine)
            line.setFrameShadow(qtw.QFrame.Sunken)
            line.setGeometry(2, 0, 2, 2*handle.height()+int(1e3))  # make sure it's long enough
        log.debug("created the splitter")
        log.info("main interface built")
    
    def buildFoldersPanel(self):
        """build the folders panel"""
        # add folder button
        self.addFolderButton = qtw.QPushButton("Add Folder")
        self.addFolderButton.setSizePolicy(qtw.QSizePolicy.Expanding, qtw.QSizePolicy.Fixed)
        self.addFolderButton.setFont(Fonts.titleFont)
        self.addFolderButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.addFolderButton.setStyleSheet("padding: 10px;")
        self.foldersPanelLayout.addWidget(self.addFolderButton)

        # separator line
        self.foldersPanelLayout.addWidget(Separator(QtCore.Qt.Horizontal))

        # folders scollable list
        self.foldersList = qtw.QScrollArea()
        self.foldersList.setWidgetResizable(True)
        self.foldersListWidget = qtw.QWidget()
        self.foldersListLayout = qtw.QVBoxLayout()
        self.foldersListWidget.setLayout(self.foldersListLayout)
        self.foldersList.setWidget(self.foldersListWidget)
        self.foldersPanelLayout.addWidget(self.foldersList)
        log.debug("created the folders panel")
    
    def buildMusicsPanel(self):
        """build the musics panel"""
        # folder name label
        self.folderNameLabel = qtw.QLabel("[FOLDER NAME]")  #TODO: remove placeholder
        self.folderNameLabel.setFont(Fonts.smallTitleFont)
        self.folderNameLabel.setSizePolicy(qtw.QSizePolicy.Expanding, qtw.QSizePolicy.Preferred)
        self.folderNameLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.musicsPanelLayout.addWidget(self.folderNameLabel)

        # number of elements label
        self.folderElementsLabel = qtw.QLabel("[NB ELEMENTS]")  #TODO: remove placeholder
        self.folderElementsLabel.setFont(Fonts.subtitleFont)
        self.folderElementsLabel.setSizePolicy(qtw.QSizePolicy.Expanding, qtw.QSizePolicy.Preferred)
        self.folderElementsLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.musicsPanelLayout.addWidget(self.folderElementsLabel)

        # separator line
        self.musicsPanelLayout.addWidget(Separator(QtCore.Qt.Horizontal))

        # musics scollable list
        self.musicsList = qtw.QScrollArea()
        self.musicsList.setWidgetResizable(True)
        self.musicsListWidget = qtw.QWidget()
        self.musicsListLayout = qtw.QVBoxLayout()
        self.musicsListWidget.setLayout(self.musicsListLayout)
        self.musicsList.setWidget(self.musicsListWidget)
        self.musicsPanelLayout.addWidget(self.musicsList)

        # separator line
        self.musicsPanelLayout.addWidget(Separator(QtCore.Qt.Horizontal))
        
        # control buttons
        self.controlButtonsWidget = qtw.QWidget()
        self.controlButtonsLayout = qtw.QHBoxLayout()
        self.controlButtonsWidget.setLayout(self.controlButtonsLayout)
        self.controlButtonsWidget.setSizePolicy(qtw.QSizePolicy.Expanding, qtw.QSizePolicy.Fixed)
        self.controlButtonsLayout.setAlignment(QtCore.Qt.AlignLeft)
        self.musicsPanelLayout.addWidget(self.controlButtonsWidget)

        # play pause button
        self.globalPlayButton = qtw.QPushButton()
        self.globalPlayButton.setFixedSize(40, 40)
        self.globalPlayButton.setIcon(QtGui.QIcon(str(themeAssetsDir / "icons" / "play.svg")))
        self.globalPlayButton.setIconSize(QtCore.QSize(30, 30))
        self.globalPlayButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.controlButtonsLayout.addWidget(self.globalPlayButton)

        # loop button
        self.loopButton = qtw.QPushButton()
        self.loopButton.setFixedSize(40, 40)
        self.loopButton.setIcon(QtGui.QIcon(str(themeAssetsDir / "icons" / "loop.svg")))
        self.loopButton.setIconSize(QtCore.QSize(30, 30))
        self.loopButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.controlButtonsLayout.addWidget(self.loopButton)

        # shuffle button
        self.shuffleButton = qtw.QPushButton()
        self.shuffleButton.setFixedSize(40, 40)
        self.shuffleButton.setIcon(QtGui.QIcon(str(themeAssetsDir / "icons" / "shuffle.svg")))
        self.shuffleButton.setIconSize(QtCore.QSize(30, 30))
        self.shuffleButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.controlButtonsLayout.addWidget(self.shuffleButton)

        self.controlButtonsLayout.addStretch()

        # sort button
        self.sortButton = qtw.QPushButton()
        self.sortButton.setFixedSize(40, 40)
        self.sortButton.setIcon(QtGui.QIcon(str(themeAssetsDir / "icons" / "sort.svg")))
        self.sortButton.setIconSize(QtCore.QSize(30, 30))
        self.sortButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.controlButtonsLayout.addWidget(self.sortButton)
        log.debug("created the musics panel")
    
    def buildPlayerPanel(self):
        """build the player panel"""
        # cover image
        self.coverWidget = qtw.QWidget()
        self.coverLayout = qtw.QHBoxLayout()
        self.coverWidget.setLayout(self.coverLayout)
        self.coverWidget.setSizePolicy(qtw.QSizePolicy.Expanding, qtw.QSizePolicy.Expanding)
        self.coverLayout.setAlignment(QtCore.Qt.AlignCenter)
        self.playerPanelLayout.addWidget(self.coverWidget)

        self.musicCover = SquareVectorLabel(themeAssetsDir / "icons" / "cover.svg")
        self.musicCover.setMaximumSize(300, 300)
        self.musicCover.setMinimumSize(100, 100)
        self.musicCover.setSizePolicy(qtw.QSizePolicy.Expanding, qtw.QSizePolicy.Expanding)
        self.musicCover.setAlignment(QtCore.Qt.AlignCenter)
        self.coverLayout.addWidget(self.musicCover)

        # music title
        self.musicTitle = qtw.QLabel("[MUSIC TITLE]")  #TODO: remove placeholder
        self.musicTitle.setFont(Fonts.titleFont)
        self.musicTitle.setAlignment(QtCore.Qt.AlignCenter)
        self.playerPanelLayout.addWidget(self.musicTitle)

        # music author
        self.musicArtist = qtw.QLabel("[AUTHOR]")  #TODO: remove placeholder
        self.musicArtist.setFont(Fonts.subtitleFont)
        self.musicArtist.setAlignment(QtCore.Qt.AlignCenter)
        self.playerPanelLayout.addWidget(self.musicArtist)

        # music progress bar layout
        self.progressWidget = qtw.QWidget()
        self.progressLayout = qtw.QHBoxLayout()
        self.progressWidget.setLayout(self.progressLayout)
        self.progressWidget.setSizePolicy(qtw.QSizePolicy.Expanding, qtw.QSizePolicy.Fixed)
        self.progressLayout.setAlignment(QtCore.Qt.AlignCenter)
        self.playerPanelLayout.addWidget(self.progressWidget)

        # music play button
        self.musicPlayButton = qtw.QPushButton()
        self.musicPlayButton.setFixedSize(40, 40)
        self.musicPlayButton.setIcon(QtGui.QIcon(str(themeAssetsDir / "icons" / "play.svg")))
        self.musicPlayButton.setIconSize(QtCore.QSize(30, 30))
        self.musicPlayButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.progressLayout.addWidget(self.musicPlayButton)

        # music progress bar
        self.musicProgressBar = MusicProgressBar()
        self.musicProgressBar.setRange(0, 100)
        self.musicProgressBar.setValue(0)
        self.musicProgressBar.setTextVisible(False)
        self.musicProgressBar.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.musicProgressBar.setSizePolicy(qtw.QSizePolicy.Expanding, qtw.QSizePolicy.Fixed)
        self.progressLayout.addWidget(self.musicProgressBar)

        # add stretch to the layout
        self.playerPanelLayout.addStretch()
        log.debug("created the player panel")

    def setupInterface(self):
        """setup the main interface"""
        return NotImplemented  #TODO
