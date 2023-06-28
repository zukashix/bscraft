# BSCraft Launcher
# Author: zukashix

# import modules
import sys
import os
import platform
import re
import json
import traceback
import shutil
import subprocess

from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QDesktopWidget, QMessageBox, QPushButton, QLineEdit
from PyQt5.QtGui import QPixmap, QFont, QFontDatabase
from PyQt5.QtCore import Qt, QThread, pyqtSignal, pyqtSlot, QObject

import modules.backUtils as Utils
from modules.mciHandler import MinecraftLauncher



class ExceptionHandler(QObject):
    """class to handle exceptions"""
    errorOccurred = pyqtSignal(str)

    def __init__(self):
        super().__init__()

    def exception_hook(self, exctype, value, tBack):
        errorLog1 = traceback.format_exception(exctype, value, tBack, None)
        errorLog2 = ''
        for err in errorLog1:
            errorLog2 = errorLog2 + err + ' '
        error_message = "An internal error occurred:\n\n" + errorLog2
        print(error_message)
        with open('./BSCraft_Launcher_Error.txt', 'w') as logfile:
            logfile.write(error_message)
        self.errorOccurred.emit(error_message)


class playGameThread(QThread):
    """Thread to handle play action"""
    finished = pyqtSignal()
    def __init__(self, username, ram, actionclass, parent=None): # get required variables from gui
        super(playGameThread, self).__init__()
        self.mcUsername = username.strip().replace(' ', '_')
        self.userMemory = ram.strip()
        self.actionclass = actionclass
        self.parentClass = parent
        self.systemMemory = Utils.getRam()

        self._progressLast = None
        self._progressMax = 0
        self._progressStatusText = ''

        try:
            self.validityData = json.load(open(APPDATA + '.bscraft/launcherValidity.json', 'r'))
        except:
            self.validityData = {
                'javaValid': False,
                'minecraftValid': False,
                'modpackValid': False
            }

            json.dump(self.validityData, open(APPDATA + '.bscraft/launcherValidity.json', 'w'))


    def _fakeMaxProgress(self, fake): # func to do nothing (used to pass as callback to mc launcher api)
        pass


    def _setProgressMax(self, maxProgress): # set maximum progress
        self._progressMax = maxProgress


    def _writeProgressStatus(self, progress): # set progress percentage
        if self._progressMax != 0:
            currentStatus = int((progress/self._progressMax)*100)
            if self._progressLast == currentStatus:
                pass
            else:
                self.parentClass.status_label.setText(self._progressStatusText.format(str(currentStatus)))
                self._progressLast = currentStatus


    def _updateValidity(self, tag: str, value: bool):
        self.validityData = json.load(open(APPDATA + '.bscraft/launcherValidity.json', 'r'))
        self.validityData[tag] = value
        json.dump(self.validityData, open(APPDATA + '.bscraft/launcherValidity.json', 'w'))


    def run(self): # run thread
        # announce that thread is run through status
        self.parentClass.status_label.setText('Processing Data...')
        self.parentClass.status_label.setStyleSheet("color: lightgreen")

        # ensure all variables are valid
        # validate username
        usernameValid = False

        if len(self.mcUsername) >= 3 and len(self.mcUsername) <= 16:
            if re.match(r'^[a-zA-Z0-9_]+$', self.mcUsername):
                usernameValid = True

        if not usernameValid:
            self.parentClass.status_label.setText("Invalid Username.")
            self.parentClass.status_label.setStyleSheet("color: orange")
            self.actionclass.isThreading = False
            self.finished.emit()
            return

        # validate ram
        try:
            self.userMemory = int(self.userMemory)
        except ValueError:
            self.parentClass.status_label.setText("Invalid RAM provided.")
            self.parentClass.status_label.setStyleSheet("color: orange")
            self.actionclass.isThreading = False
            self.finished.emit()
            return

        if self.systemMemory <= self.userMemory:
            self.parentClass.status_label.setText("Too much RAM provided.")
            self.parentClass.status_label.setStyleSheet("color: orange")
            self.actionclass.isThreading = False
            self.finished.emit()
            return


        # check for internet and downloaded files
        if not Utils.checkInternet() and not self.validityData['javaValid'] and not self.validityData['minecraftValid'] and not self.validityData['modpackValid']:
            self.parentClass.status_label.setText("Server unreachable & files missing.")
            self.parentClass.status_label.setStyleSheet("color: orange")
            self.actionclass.isThreading = False
            self.finished.emit()
            return

        progressCallback = {"setStatus": self._fakeMaxProgress, "setProgress": self._writeProgressStatus, "setMax": self._setProgressMax}
        self.Launcher = MinecraftLauncher(APPDATA + '.bscraft', self.mcUsername, self.userMemory, progressCallback)

        # begin installation tasks
        # install java
        if not self.validityData["javaValid"]:
            self._progressStatusText = 'Installing Java... [{}%]'
            self.parentClass.status_label.setStyleSheet("color: lightgreen")

            try:
                shutil.rmtree(APPDATA + '.bscraft/runtime/')
            except FileNotFoundError:
                pass
            
            self.Launcher.installJava()
            
            self._updateValidity('javaValid', True)


        # install core minecraft
        if not self.validityData["minecraftValid"]:
            self._progressStatusText = 'Installing Minecraft... [{}%]'
            self.parentClass.status_label.setStyleSheet("color: lightgreen")
            
            self.Launcher.installMinecraft()
            
            self._updateValidity('minecraftValid', True)


        # install modpack files
        if not self.validityData["modpackValid"]:
            self.parentClass.status_label.setText('Installing Modpack...') 
            # self._progressStatusText = 'Installing Modpack... [{}%]'
            self.parentClass.status_label.setStyleSheet("color: lightgreen")
            
            self.Launcher.installModpack()
            
            self._updateValidity('modpackValid', True)


        # announce and init required launcher functions
        self.parentClass.status_label.setText('Initializing Minecraft...')
        self.parentClass.status_label.setStyleSheet("color: lightgreen")
        spCommand = self.Launcher.getRunCMD()

        # hide launcher window and start game. show window again if game exits and end thread
        self.parentClass.hide()
        subprocess.call(spCommand)
        self.parentClass.show()
        self.parentClass.activateWindow()

        self.parentClass.status_label.setText("Ready!")
        self.parentClass.status_label.setStyleSheet("color: lightgreen")

        self.actionclass.isThreading = False
        self.finished.emit()


class LauncherActions():
    """class to organize all actions performed by the launcher"""
    def __init__(self, selfObj): # get mainWindow object
        self.isThreading = False
        self.selfObj = selfObj    

    def quitLauncher(self): # funcion to exit launcher
        self.selfObj.quit_button.setStyleSheet('color: gray; background-color: #fc8eac; border: 3px solid #e75480')
        if self.isThreading:
            QMessageBox.information(self.selfObj, "BSCraft Launcher", "Cannot exit, a launcher task is running.")
            self.selfObj.quit_button.setStyleSheet('color: white; background-color: #fc8eac; border: 3px solid #e75480')
        else:
            QApplication.quit()

    def _deleteThread(self): # function to delete thread after task is complete
        if self.thread is not None:
            self.thread.finished.disconnect(self._deleteThread)
            self.thread.deleteLater()
            self.thread = None

    def playGame(self, username, ram): # function to start thread if play button is clicked
        self.selfObj.play_button.setEnabled(False) # disable play button if thread already running
        self.selfObj.play_button.setStyleSheet('color: gray; background-color: #fc8eac; border: 3px solid #e75480')
        self.isThreading = True
        self.thread = playGameThread(username, ram, self, parent=self.selfObj)
        self.thread.finished.connect(lambda: self.selfObj.play_button.setEnabled(True))
        self.thread.finished.connect(lambda: self.selfObj.play_button.setStyleSheet('color: white; background-color: #fc8eac; border: 3px solid #e75480'))
        self.thread.finished.connect(self._deleteThread)
        self.thread.start()



class DisplayGUI(QMainWindow):
    """class to provide GUI to bootstrapper"""
    def __init__(self): 
        # init and set variables
        super(DisplayGUI, self).__init__()
        self.actionclass = LauncherActions(self)
        self.exception_handler = ExceptionHandler()
        self.exception_handler.errorOccurred.connect(self.display_error)

        ram = Utils.getRam()
        if ram < 5000:
            ramPlaceholder = '3072'
        else:
            ramPlaceholder = '6144'

        # load external resources
        QFontDatabase.addApplicationFont("resources/Minecraftia.ttf")

        # Set window properties
        self.setWindowTitle("BSCraft Launcher")
        self.setWindowFlag(Qt.FramelessWindowHint)
        #self.setGeometry(0, 0, 800, 400)
        self.resize(800, 450)
        self._centerWindow()

        # Set background image
        self.window_bg = QLabel(self)
        self.window_bg.setGeometry(0, 0, 800, 450)
        self.window_bg.setPixmap(QPixmap("resources/bgimg.jpg"))

        # Set labels
        self.status_label = QLabel(self)
        self.status_label.setGeometry(40, 400, 750, 50)
        self.status_label.setFont(QFont("Minecraftia", 15))
        self.status_label.setText("Ready!")
        self.status_label.setStyleSheet("color: lightgreen")

        self.username_sign_label = QLabel(self)
        self.username_sign_label.setGeometry(475, 240, 350, 40)
        self.username_sign_label.setFont(QFont("Minecraftia", 15))
        self.username_sign_label.setText("Username:")
        self.username_sign_label.setStyleSheet("color: white")

        self.ram_sign_label = QLabel(self)
        self.ram_sign_label.setGeometry(475, 165, 350, 40)
        self.ram_sign_label.setFont(QFont("Minecraftia", 15))
        self.ram_sign_label.setText("RAM [In MB]:")
        self.ram_sign_label.setStyleSheet("color: white")

        # set action buttons
        self.play_button = QPushButton("Play!", self)
        self.play_button.clicked.connect(lambda: self.actionclass.playGame(self.username_textbox.text(), self.ram_textbox.text()))
        self.play_button.setGeometry(450, 350, 100, 50)
        self.play_button.setFont(QFont("Minecraftia", 15))
        self.play_button.setStyleSheet('color: white; background-color: #fc8eac; border: 3px solid #e75480')

        self.quit_button = QPushButton("Quit", self)
        self.quit_button.clicked.connect(self.actionclass.quitLauncher)
        self.quit_button.setGeometry(600, 350, 100, 50)
        self.quit_button.setFont(QFont("Minecraftia", 15))
        self.quit_button.setStyleSheet('color: white; background-color: #fc8eac; border: 3px solid #e75480')

        # set textboxes
        self.username_textbox = QLineEdit(self)
        self.username_textbox.setGeometry(475, 275, 200, 30)
        self.username_textbox.setFont(QFont("Minecraftia", 15))
        #self.username_textbox.setText("Player0")
        self.username_textbox.setStyleSheet('color: white; background-color: #fc8eac; border: 3px solid #e75480')

        self.ram_textbox = QLineEdit(self)
        self.ram_textbox.setGeometry(475, 200, 200, 30)
        self.ram_textbox.setFont(QFont("Minecraftia", 15))
        self.ram_textbox.setText(ramPlaceholder)
        self.ram_textbox.setStyleSheet('color: white; background-color: #fc8eac; border: 3px solid #e75480')


    # function to help center the window on any resolution 
    def _centerWindow(self):                     
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


    # function to display exceptions
    @pyqtSlot(str)
    def display_error(self, error_message):
        QMessageBox.critical(None, "BSCraft Launcher", error_message)
        QApplication.quit()


if __name__ == "__main__":
    # configure primary directory as per os
    plat = platform.system().lower()
    if 'win' in plat:
        APPDATA = os.getenv("APPDATA").replace("\\", "/") + '/' # windows
    else:
        APPDATA = os.getenv("HOME") + '/' # linux

    # make .bscraft working folder if it doesnt exist
    try:
        os.makedirs(APPDATA + '.bscraft/')
    except FileExistsError:
        pass

    # run app
    app = QApplication(sys.argv)
    window = DisplayGUI()
    sys.excepthook = window.exception_handler.exception_hook
    window.show()
    sys.exit(app.exec_())
