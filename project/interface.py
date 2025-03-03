from constants import *
from widgets import *
import PyQt5.QtWidgets as qtw
from PyQt5 import QtCore, QtGui
from pathlib import Path
import random as rd
import logging
import eyed3
import glob
import json
import vlc

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
        self.mainSplitter.setSizes([300, 400, 400])

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
        self.foldersList.setFrameShape(qtw.QFrame.NoFrame)
        self.foldersListWidget = qtw.QWidget()
        self.foldersListLayout = qtw.QVBoxLayout()
        self.foldersListLayout.setAlignment(QtCore.Qt.AlignTop)
        self.foldersListWidget.setLayout(self.foldersListLayout)
        self.foldersList.setWidget(self.foldersListWidget)
        self.foldersPanelLayout.addWidget(self.foldersList)
    
    def buildMusicsPanel(self):
        """build the musics panel"""
        # folder name label
        self.folderNameLabel = qtw.QLabel("[FOLDER NAME]")
        self.folderNameLabel.setFont(Fonts.smallTitleFont)
        self.folderNameLabel.setSizePolicy(qtw.QSizePolicy.Expanding, qtw.QSizePolicy.Preferred)
        self.folderNameLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.musicsPanelLayout.addWidget(self.folderNameLabel)

        # number of elements label
        self.folderElementsLabel = qtw.QLabel("[NB ELEMENTS]")
        self.folderElementsLabel.setFont(Fonts.subtitleFont)
        self.folderElementsLabel.setSizePolicy(qtw.QSizePolicy.Expanding, qtw.QSizePolicy.Preferred)
        self.folderElementsLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.musicsPanelLayout.addWidget(self.folderElementsLabel)

        # separator line
        self.musicsPanelLayout.addWidget(Separator(QtCore.Qt.Horizontal))

        # musics scollable list
        self.musicsList = qtw.QScrollArea()
        self.musicsList.setWidgetResizable(True)
        self.musicsList.setFrameShape(qtw.QFrame.NoFrame)
        self.musicsListWidget = qtw.QWidget()
        self.musicsListLayout = qtw.QVBoxLayout()
        self.musicsListLayout.setAlignment(QtCore.Qt.AlignTop)
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
        self.loopButton.setCheckable(True)
        self.loopButton.setIconSize(QtCore.QSize(30, 30))
        self.loopButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.controlButtonsLayout.addWidget(self.loopButton)

        # shuffle button
        self.shuffleButton = qtw.QPushButton()
        self.shuffleButton.setFixedSize(40, 40)
        self.shuffleButton.setCheckable(True)
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
        #self.controlButtonsLayout.addWidget(self.sortButton)  #TODO: implement this, hidden for now

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
        self.musicTitle = qtw.QLabel("[MUSIC TITLE]")
        self.musicTitle.setFont(Fonts.titleFont)
        self.musicTitle.setAlignment(QtCore.Qt.AlignCenter)
        self.playerPanelLayout.addWidget(self.musicTitle)

        # music author
        self.musicArtist = qtw.QLabel("[AUTHOR]")
        self.musicArtist.setFont(Fonts.subtitleFont)
        self.musicArtist.setAlignment(QtCore.Qt.AlignCenter)
        self.playerPanelLayout.addWidget(self.musicArtist)

        # music progress layout
        self.progressWidget = qtw.QWidget()
        self.progressLayout = qtw.QHBoxLayout()
        self.progressWidget.setLayout(self.progressLayout)
        self.progressWidget.setSizePolicy(qtw.QSizePolicy.Expanding, qtw.QSizePolicy.Fixed)
        self.progressLayout.setAlignment(QtCore.Qt.AlignTop)
        self.playerPanelLayout.addWidget(self.progressWidget)

        # music play button
        self.musicPlayButtonWidget = qtw.QWidget()
        self.musicPlayButtonLayout = qtw.QVBoxLayout()
        self.musicPlayButtonWidget.setLayout(self.musicPlayButtonLayout)
        self.musicPlayButtonWidget.setSizePolicy(qtw.QSizePolicy.Fixed, qtw.QSizePolicy.Fixed)
        self.progressLayout.addWidget(self.musicPlayButtonWidget)

        self.musicPlayButton = qtw.QPushButton()
        self.musicPlayButton.setFixedSize(40, 40)
        self.musicPlayButton.setIcon(QtGui.QIcon(str(themeAssetsDir / "icons" / "play.svg")))
        self.musicPlayButton.setIconSize(QtCore.QSize(30, 30))
        self.musicPlayButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.musicPlayButtonLayout.addWidget(self.musicPlayButton)
        self.musicPlayButtonLayout.addSpacing(45)

        # music progress bar
        self.progressBarWidget = qtw.QWidget()
        self.progressBarLayout = qtw.QVBoxLayout()
        self.progressBarWidget.setLayout(self.progressBarLayout)
        self.progressBarWidget.setSizePolicy(qtw.QSizePolicy.Expanding, qtw.QSizePolicy.Fixed)
        self.progressLayout.addWidget(self.progressBarWidget)

        self.musicProgressBar = MusicProgressBar()
        self.musicProgressBar.setRange(0, 100)
        self.musicProgressBar.setValue(0)
        self.musicProgressBar.setStyleSheet(f"""QProgressBar {{ border: 2px solid gray; border-radius: 5px; background-color: transparent; }}
                                                QProgressBar::chunk {{ background-color: {"white" if colorMode == "dark" else "black"}; border-radius: 3px; }}""")
        self.musicProgressBar.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.musicProgressBar.setSizePolicy(qtw.QSizePolicy.Expanding, qtw.QSizePolicy.Fixed)
        self.progressBarLayout.addWidget(self.musicProgressBar)

        # music time labels
        self.musicTimeWidget = qtw.QWidget()
        self.musicTimeLayout = qtw.QHBoxLayout()
        self.musicTimeWidget.setLayout(self.musicTimeLayout)
        self.musicTimeWidget.setSizePolicy(qtw.QSizePolicy.Expanding, qtw.QSizePolicy.Fixed)
        self.progressBarLayout.addWidget(self.musicTimeWidget)

        self.musicCurrentTimeLabel = qtw.QLabel("[0:00]")
        self.musicCurrentTimeLabel.setFont(Fonts.bigTextFont)
        self.musicTimeLayout.addWidget(self.musicCurrentTimeLabel)

        self.musicTimeLayout.addStretch()

        self.musicTotalTimeLabel = qtw.QLabel("[0:00]")
        self.musicTotalTimeLabel.setFont(Fonts.bigTextFont)
        self.musicTimeLayout.addWidget(self.musicTotalTimeLabel)

        # separator for the buttons below
        self.playerPanelLayout.addWidget(Separator(QtCore.Qt.Horizontal))

        # rename button
        self.renameButton = qtw.QPushButton("Set Title")
        self.renameButton.setFont(Fonts.titleFont)
        self.renameButton.setFixedHeight(50)
        self.renameButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.playerPanelLayout.addWidget(self.renameButton)

        # set author button
        self.setAuthorButton = qtw.QPushButton("Set Author")
        self.setAuthorButton.setFont(Fonts.titleFont)
        self.setAuthorButton.setFixedHeight(50)
        self.setAuthorButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.playerPanelLayout.addWidget(self.setAuthorButton)

        # set cover button
        self.setCoverButton = qtw.QPushButton("Set Cover")
        self.setCoverButton.setFont(Fonts.titleFont)
        self.setCoverButton.setFixedHeight(50)
        self.setCoverButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.playerPanelLayout.addWidget(self.setCoverButton)

        # add stretch to the layout
        self.playerPanelLayout.addStretch()
        log.debug("created the player panel")

    def setupInterface(self):
        """setup the main interface"""
        if not configFile.exists():
            # if first launch
            log.info("no config file found, creating initial config")
            self.config = {
                "folders": [str(Path.home() / "Music")] if (Path.home() / "Music").exists() else [],
                "loop": False,
                "shuffle": False,
                "sort": "+name",
                "autoplay": False
            }
            self.saveConfig()
        self.config = json.load(open(configFile))
        log.debug("loaded the config file")
        
        # show only necesary panels
        self.musicsPanel.hide()
        self.playerPanel.hide()
        log.debug("hided the musics and player panels")

        # set the buttons
        loopIcon = "loop_none.svg" if self.config["loop"] == False else "loop_down.svg" if self.config["loop"] == "down" else "loop_one.svg" if self.config["loop"] == "one" else "loop.svg"
        self.loopButton.setIcon(QtGui.QIcon(str(themeAssetsDir / "icons" / loopIcon)))
        if self.config["loop"] == False:
            self.loopButton.setChecked(False)
        else:
            self.loopButton.setChecked(True)
        self.shuffleButton.setChecked(self.config["shuffle"])
        log.debug("set the buttons")

        # useful variables
        self.folderWidgets = []
        self.musicWidgets = []

        self.currentFolder = None
        self.currentMusic = None
        self.musicPlaying = False
        self.musicObject = None
        self.progressTimer = QtCore.QTimer()
        self.progressTimer.timeout.connect(self.updateMusicProgress)
        self.loopMode = self.config["loop"]
        self.shuffleMode = self.config["shuffle"]
        self.sortMode = self.config["sort"]
        self.musicCurrentTime = 0
        self.musicTotalTime = 0
        self.alreadyPlayed = []
        log.debug("set the variables")

        # connect signals
        self.addFolderButton.clicked.connect(self.addFolder)
        self.globalPlayButton.clicked.connect(self.globalPlay)
        self.loopButton.clicked.connect(self.loopState)
        self.shuffleButton.clicked.connect(self.shuffleState)
        self.sortButton.clicked.connect(self.sortState)
        self.musicPlayButton.clicked.connect(self.musicPlay)
        self.musicProgressBar.clickedValue.connect(self.musicSliderPressed)
        self.renameButton.clicked.connect(self.setTitle)
        self.setAuthorButton.clicked.connect(self.setAuthor)
        self.setCoverButton.clicked.connect(self.setCover)
        log.debug("connected signals")

        # load the folders
        self.loadFolders()
        log.info("interface setup done")
    
    def saveConfig(self):
        """save the config to the config file"""
        with open(configFile, "w") as f:
            json.dump(self.config, f, indent=4)
        log.debug("saved the config file")
    
    def loadFolders(self):
        """load the folders from the config file into the interface"""
        # remove the previous folders
        for widget in self.folderWidgets:
            widget.deleteLater()
        
        # load the folders
        self.folderWidgets = []
        for folder in self.config["folders"]:
            self.folderWidgets.append(FolderWidget(Path(folder)))
            self.folderWidgets[-1].wasSelected.connect(self.selectFolder)
            self.folderWidgets[-1].wasRemoved.connect(self.removeFolder)
            self.foldersListLayout.addWidget(self.folderWidgets[-1])
        log.debug("loaded the folders")
    
    def selectFolder(self, folder:Path):
        """select a folder and show its musics"""
        if self.currentFolder == folder:
            return  # do nothing if the folder is already selected
        # unselect the previous folder
        for widget in self.folderWidgets:
            if widget.folderPath != folder:
                widget.setSelected(False)
        self.currentFolder = folder
        self.alreadyPlayed = []
        self.currentMusic = None
        self.unloadMusic()
        self.musicPlaying = False
        # update the interface with the new folder
        self.musicsPanel.show()
        self.playerPanel.hide()
        self.loadMusics()
    
    def removeFolder(self, folder:Path):
        """remove a folder from the folders list"""
        confirm = qtw.QMessageBox.warning(self, "Remove Folder", f'Are you sure you want to remove "{folder}"?\nNote: this won\'t delete the folder itself, just remove it from the list', qtw.QMessageBox.Yes | qtw.QMessageBox.Cancel)
        if confirm == qtw.QMessageBox.Yes:
            for i in range(len(self.config["folders"])):
                if Path(self.config["folders"][i]) == folder:
                    self.config["folders"].pop(i)
            self.saveConfig()
            if self.currentFolder == folder:
                self.currentFolder = None
                self.alreadyPlayed = []
                self.currentMusic = None
                self.unloadMusic()
                self.musicPlaying = False
                self.musicsPanel.hide()
                self.playerPanel.hide()
            self.loadFolders()
            # reselect the folder after the update
            if self.currentFolder:
                for widget in self.folderWidgets:
                    if widget.folderPath == Path(self.currentFolder):
                        widget.setSelected(True)
                        break
            log.info(f"removed the folder {folder}")
    
    def loadMusics(self):
        """list and load the musics from the selected folder"""
        # remove the previous musics
        for widget in self.musicWidgets:
            widget.deleteLater()
        self.musicWidgets = []

        # list the musics
        musics = []
        for dir in glob.glob(str(self.currentFolder/"*")):
            if Path(dir).is_file() and Path(dir).suffix in supportedAudioFormats:
                musics.append(Path(dir))
        log.debug(f"listed the musics for the folder {self.currentFolder}")

        # update the folder name and number of elements
        self.folderNameLabel.setText(self.currentFolder.name)
        self.folderElementsLabel.setText(f"{len(musics)} Musics")

        # load the music widgets
        for music in musics:
            self.musicWidgets.append(MusicWidget(music))
            self.musicWidgets[-1].wasSelected.connect(self.selectMusic)
            self.musicsListLayout.addWidget(self.musicWidgets[-1])
        log.debug(f"loaded the musics for the folder {self.currentFolder}")
    
    def selectMusic(self, music:Path):
        """select a music and show its details and player panel"""
        if self.currentMusic == music:
            return  # do nothing if the music is already selected
        # unselect the previous music
        for widget in self.musicWidgets:
            if widget.musicPath != music:
                widget.setSelected(False)
        self.currentMusic = music
        self.unloadMusic()
        self.musicPlaying = False
        # update the interface with the new music
        self.playerPanel.show()
        self.updateMusicPlayer(music)
    
    def updateMusicPlayer(self, music:Path):
        """update the player panel with the selected music"""
        # open the music metadata and get the info
        audioFile = eyed3.load(music)
        if audioFile.tag:
            title = audioFile.tag.title if audioFile.tag.title else music.stem
            artist = audioFile.tag.artist if audioFile.tag.artist else None
            cover = audioFile.tag.images[0].image_data if audioFile.tag.images else None
        else:
            title = music.stem
            artist = None
            cover = None
        media = vlc.Media(str(music))
        media.parse()
        duration = int(media.get_duration() / 1000)

        # load the music
        self.musicObject = vlc.MediaPlayer(str(music))
        # start playing briefly to load the media
        self.musicObject.audio_set_volume(0)
        self.musicObject.play()
        while not self.musicObject.get_state() == vlc.State.Playing:
            pass
        self.musicObject.pause()
        self.musicObject.set_time(0)
        self.musicObject.audio_set_volume(100)
        log.debug(f"loaded the music")
        
        # update the interface
        self.musicTitle.setText(title)
        if artist:
            self.musicArtist.setText(artist)
        else:
            self.musicArtist.setText("")
        if cover:
            self.musicCover.setPixmap(QtGui.QPixmap.fromImage(QtGui.QImage.fromData(cover)))
        else:
            self.musicCover.setVector(themeAssetsDir / "icons" / "cover.svg")
        self.musicProgressBar.setRange(0, duration)
        self.musicProgressBar.setValue(0)
        self.musicCurrentTimeLabel.setText("0:00")
        self.musicTotalTimeLabel.setText(f"{duration//60}:{duration%60:02}")
        log.debug(f"updated the player panel for the music {music}")
    
    def addFolder(self):
        """add a folder to the folders list"""
        # open a dialog to select a folder
        folder = qtw.QFileDialog.getExistingDirectory(self, "Select music folder", str(Path.home()))
        if not folder:
            return  # do nothing if no folder was selected
        # add the folder to the config and interface
        self.config["folders"].append(folder)
        self.saveConfig()
        self.loadFolders()
        # reselect the folder after the update
        if self.currentFolder:
            for widget in self.folderWidgets:
                if widget.folderPath == Path(self.currentFolder):
                    widget.setSelected(True)
                    break
        log.info(f"added the folder {folder}")

    def loopState(self):
        """change the loop state"""
        if self.loopMode == False:
            self.loopMode = "down"  # play from top to bottom until the end, or play everything once if shuffle is on
            self.loopButton.setIcon(QtGui.QIcon(str(themeAssetsDir / "icons" / "loop_down.svg")))
            self.loopButton.setChecked(True)
            self.config["loop"] = "down"
            self.saveConfig()

        elif self.loopMode == "down":
            self.loopMode = "one"  # play the current music on repeat
            self.loopButton.setIcon(QtGui.QIcon(str(themeAssetsDir / "icons" / "loop_one.svg")))
            self.loopButton.setChecked(True)
            self.config["loop"] = "one"
            self.saveConfig()

        elif self.loopMode == "one":
            self.loopMode = "all"  # play everything on repeat, or play a random music on repeat if shuffle is on
            self.loopButton.setIcon(QtGui.QIcon(str(themeAssetsDir / "icons" / "loop.svg")))
            self.loopButton.setChecked(True)
            self.config["loop"] = "all"
            self.saveConfig()

        else:
            self.loopMode = False  # play until the end of the music then stop
            self.loopButton.setIcon(QtGui.QIcon(str(themeAssetsDir / "icons" / "loop_none.svg")))
            self.loopButton.setChecked(False)
            self.config["loop"] = False
            self.saveConfig()

    def shuffleState(self):
        """change the shuffle state"""
        if self.shuffleMode:
            self.shuffleMode = False
            self.shuffleButton.setChecked(False)
            self.config["shuffle"] = False
            self.saveConfig()
        else:
            self.shuffleMode = True
            self.shuffleButton.setChecked(True)
            self.config["shuffle"] = True
            self.saveConfig()

    def sortState(self):
        """change the sort state"""
        return NotImplemented  #TODO: implement this

    def musicPlay(self):
        """play or pause the music"""
        if self.musicPlaying:
            self.musicPlaying = False
            self.musicPlayButton.setIcon(QtGui.QIcon(str(themeAssetsDir / "icons" / "play.svg")))
            self.globalPlayButton.setIcon(QtGui.QIcon(str(themeAssetsDir / "icons" / "play.svg")))
            self.musicObject.pause()
            self.progressTimer.stop()
            log.info("paused the music")
        else:
            self.musicPlaying = True
            self.musicPlayButton.setIcon(QtGui.QIcon(str(themeAssetsDir / "icons" / "pause.svg")))
            self.globalPlayButton.setIcon(QtGui.QIcon(str(themeAssetsDir / "icons" / "pause.svg")))
            self.musicObject.play()
            self.progressTimer.start(10)
            log.info("played the music")
    
    def globalPlay(self):
        """play or pause the music from the global play button"""
        if self.playerPanel.isVisible():  # act as the basic play/pause button if the player panel is visible
            self.musicPlay()
        else:  # play the first or a random music if the player panel is hidden
            if self.shuffleMode:
                music = rd.choice(self.musicWidgets)
            else:
                music = self.musicWidgets[0]
            self.selectMusic(music.musicPath)
            music.setSelected(True)
            self.musicPlay()
    
    def unloadMusic(self):
        """unload the music from the player"""
        # stop playing if needed
        if self.musicPlaying:
            self.musicPlay()
        if self.musicObject:
            self.musicObject.release()
            self.musicObject = None

    def musicSliderPressed(self, value:float):
        """change the music time"""
        value = round(value)
        self.musicCurrentTime = value
        # change the music time label
        self.musicCurrentTimeLabel.setText(f"{value//60}:{value%60:02}")
        
        # change the music time
        if self.musicObject:
            self.musicObject.set_time(value * 1000)
        log.info(f"changed the music time to {value}")
    
    def updateMusicProgress(self):
        """update the music progress bar and handles the end of the music"""
        # update the progress bar
        if self.musicObject:
            currentTime = int(self.musicObject.get_time() / 1000)
            self.musicProgressBar.setValue(currentTime)
            self.musicCurrentTimeLabel.setText(f"{currentTime//60}:{currentTime%60:02}")
        
        # handle the end of the music
        if self.musicObject.get_state() == vlc.State.Ended:
            self.musicPlay()  # stop the music

            if self.loopMode == False:  # simply stop the music
                self.updateMusicPlayer(self.currentMusic)
            
            elif self.loopMode == "one":  # restart the music
                self.updateMusicPlayer(self.currentMusic)
                self.musicPlay()
            
            elif self.loopMode == "down" or self.loopMode == "all":  # play the next music or a random one, all restarts at the beginning when reached the end
                if self.shuffleMode:  # play a random music
                    self.alreadyPlayed.append(self.currentMusic)
                    candidates = [music for music in self.musicWidgets if ((music.musicPath not in self.alreadyPlayed) or (self.loopMode == "all")) and music.musicPath != self.currentMusic]  # if down, choose candidates, else take the whole list without the current music
                    if not candidates:  # stop there is there's no more music to play
                        self.updateMusicPlayer(self.currentMusic)
                        self.alreadyPlayed = []
                    else:
                        music = rd.choice(candidates)
                        self.selectMusic(music.musicPath)
                        music.setSelected(True)
                        self.musicPlay()

                else:  # play the next music
                    for i in range(len(self.musicWidgets)):
                        if self.musicWidgets[i].musicPath == self.currentMusic:
                            if i == len(self.musicWidgets) - 1:
                                if self.loopMode == "all":  # restart if reached the end
                                    self.selectMusic(self.musicWidgets[0].musicPath)
                                    self.musicWidgets[0].setSelected(True)
                                    self.musicPlay()
                                else:
                                    self.updateMusicPlayer(self.musicWidgets[i].musicPath)  # stop if reached the end
                            else:
                                self.selectMusic(self.musicWidgets[i+1].musicPath)
                                self.musicWidgets[i+1].setSelected(True)
                                self.musicPlay()
                            break

    def setTitle(self):
        """set the music title"""
        # ask for the new title
        title, ok = qtw.QInputDialog.getText(self, "Set Title", "Enter the new title:")
        if not ok or not title:
            return
        musicPath = self.currentMusic

        # change the metadata
        audioFile = eyed3.load(self.currentMusic)
        if audioFile.tag is None:
            audioFile.initTag()
        audioFile.tag.title = title
        audioFile.tag.save()
        self.loadMusics()
        self.updateMusicPlayer(musicPath)
        # reselect the music after the update
        for widget in self.musicWidgets:
            if widget.musicPath == musicPath:
                widget.setSelected(True)
                break
        log.info(f"changed the title of the music to {title}")

    def setAuthor(self):
        """set the music author"""
        # ask for the new author
        author, ok = qtw.QInputDialog.getText(self, "Set Author", "Enter the new author:")
        if not ok or not author:
            return
        if "/" in author or "\\" in author:
            qtw.QMessageBox.warning(self, "Invalid Input", "Author name cannot contain '/' or '\\' characters.")
            return
        if not ok or not author:
            return
        musicPath = self.currentMusic

        # change the metadata
        audioFile = eyed3.load(self.currentMusic)
        if audioFile.tag is None:
            audioFile.initTag()
        audioFile.tag.artist = author
        audioFile.tag.save()
        self.loadMusics()
        self.updateMusicPlayer(musicPath)
        # reselect the music after the update
        for widget in self.musicWidgets:
            if widget.musicPath == musicPath:
                widget.setSelected(True)
                break
        log.info(f"changed the author of the music to {author}")

    def setCover(self):
        """set the music cover"""
        # open a dialog to select an image
        cover, _ = qtw.QFileDialog.getOpenFileName(self, "Select Cover", str(Path.home()), "Images (*.png *.jpg *.jpeg *.gif *.webp *.tiff)")
        if not cover:
            return
        cover = Path(cover)
        if not cover.exists():
            qtw.QMessageBox.critical(self, "Error", "The selected file doesn't exist")
            return
        musicPath = self.currentMusic

        # change the metadata
        audioFile = eyed3.load(self.currentMusic)
        if audioFile.tag is None:
            audioFile.initTag()
        mimetype = f"image/{'jpeg' if cover.suffix[1:] == 'jpg' else cover.suffix[1:]}"
        audioFile.tag.images.set(eyed3.id3.frames.ImageFrame.FRONT_COVER, open(cover, "rb").read(), mimetype)
        audioFile.tag.save()
        self.loadMusics()
        self.updateMusicPlayer(musicPath)
        # reselect the music after the update
        for widget in self.musicWidgets:
            if widget.musicPath == musicPath:
                widget.setSelected(True)
                break
    
    def keyPressEvent(self, event:QtGui.QKeyEvent):
        """handle the key press events"""
        # handle the space key to play/pause the music
        if event.key() == QtCore.Qt.Key_Space and self.playerPanel.isVisible():
            self.musicPlay()
            event.accept()
        else:
            super().keyPressEvent(event)
