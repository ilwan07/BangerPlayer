import PyQt5.QtWidgets as qtw
from PyQt5 import QtGui, QtCore
import logging

log = logging.getLogger(__name__)


class Window(qtw.QMainWindow):
    """main window class for the BangerPlayer application"""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Banger Player")
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
        return NotImplemented  #TODO
    
    def buildMusicsPanel(self):
        """build the musics panel"""
        return NotImplemented  #TODO
    
    def buildPlayerPanel(self):
        """build the player panel"""
        return NotImplemented  #TODO

    def setupInterface(self):
        """setup the main interface"""
        return NotImplemented  #TODO
