# Module to handle backend/threading for BSCraft Launcher
# Author: zukashix

# import modules
import os
import re
import json
import shutil
import subprocess

from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.QtCore import QThread, pyqtSignal
import requests

import modules.backUtils as Utils
from modules.mciHandler import MinecraftLauncher


APPDATA = None


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

        if os.path.isfile(APPDATA + '.bscraft/launcherValidity.json'):
            self.validityData = json.load(open(APPDATA + '.bscraft/launcherValidity.json', 'r'))
        else:
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


    def _setStatusText(self, text: str, color: str):
        self.parentClass.status_label.setText(text)
        self.parentClass.status_label.setStyleSheet("color: {}".format(color))


    def _updateValidity(self, tag: str, value: bool):
        self.validityData = json.load(open(APPDATA + '.bscraft/launcherValidity.json', 'r'))
        self.validityData[tag] = value
        json.dump(self.validityData, open(APPDATA + '.bscraft/launcherValidity.json', 'w'))


    def run(self): # run thread
        # announce that thread is run through status
        self._setStatusText('Processing Data...', 'lightgreen')

        # ensure all variables are valid
        # validate username
        usernameValid = False

        if len(self.mcUsername) >= 3 and len(self.mcUsername) <= 16:
            if re.match(r'^[a-zA-Z0-9_]+$', self.mcUsername):
                usernameValid = True

        if not usernameValid:
            self._setStatusText('Invalid Username.', 'orange')
            self.actionclass.isThreading = False
            self.finished.emit()
            return

        # validate ram
        try:
            self.userMemory = int(self.userMemory)
        except ValueError:
            self._setStatusText('Invalid RAM provided.', 'orange')
            self.actionclass.isThreading = False
            self.finished.emit()
            return

        if self.systemMemory <= self.userMemory:
            self._setStatusText('Too much RAM provided.', 'orange')
            self.actionclass.isThreading = False
            self.finished.emit()
            return


        # save user data in file
        userData = {
            'usernamePlaceholder': self.mcUsername, 'ramPlaceholder': str(self.userMemory)
        }

        json.dump(userData, open(APPDATA + '.bscraft/BSCUserData.json', 'w'))


        # check for internet and downloaded files
        if not Utils.checkInternet() and not self.validityData['javaValid'] and not self.validityData['minecraftValid'] and not self.validityData['modpackValid']:
            self._setStatusText("Server unreachable & files missing.", 'orange')
            self.actionclass.isThreading = False
            self.finished.emit()
            return
        

        if not Utils.checkInternet():
            if os.path.isfile(APPDATA + '.bscraft/lastRepoData.json'):
                repoData = json.load(open(APPDATA + '.bscraft/lastRepoData.json', 'r'))
            else:
                self._setStatusText("Server unreachable & files missing.", 'orange')
                self.actionclass.isThreading = False
                self.finished.emit()
                return
            
        else:
            repoData = requests.get("https://updater.braydenedgar.com/BSCraft/launcher_data.json", headers=Utils.headers).json()
            json.dump(repoData, open(APPDATA + '.bscraft/lastRepoData.json', 'w'))


        progressCallback = {"setStatus": self._fakeMaxProgress, "setProgress": self._writeProgressStatus, "setMax": self._setProgressMax, "setText": self._setStatusText}
        self.Launcher = MinecraftLauncher(APPDATA + '.bscraft', self.mcUsername, self.userMemory, progressCallback, repoData)

        # begin installation tasks
        # install java
        if not self.validityData["javaValid"]:
            self._progressStatusText = 'Installing Java... [{}%]'
            self.parentClass.status_label.setStyleSheet("color: lightgreen")

            if os.path.isdir(APPDATA + '.bscraft/runtime/'):
                shutil.rmtree(APPDATA + '.bscraft/runtime/')
            
            self.Launcher.installJava()
            
            self._updateValidity('javaValid', True)


        # install core minecraft
        if not self.validityData["minecraftValid"]:
            self._progressStatusText = 'Installing Minecraft... [{}%]'
            self.parentClass.status_label.setStyleSheet("color: lightgreen")
            
            self.Launcher.installMinecraft()
            
            self._updateValidity('minecraftValid', True)


        # install modpack files
        
        if Utils.checkInternet():
            self._progressStatusText = "Downloading Modpack... [{}%]"
            self.parentClass.status_label.setStyleSheet("color: lightgreen")

            self.Launcher.installModpack()

            self._updateValidity('modpackValid', True)


        # announce and init required launcher functions
        self._setStatusText("Initializing Minecraft...", 'lightgreen')
        spCommand = self.Launcher.getRunCMD()

        # hide launcher window and start game. show window again if game exits and end thread
        self.parentClass.hide()

        subprocess.call(spCommand)

        self.parentClass.show()
        self.parentClass.activateWindow()

        self._setStatusText("Ready!", 'lightgreen')

        self.actionclass.isThreading = False
        self.finished.emit()



class LauncherActions():
    """class to organize all actions performed by the launcher"""
    def __init__(self, appdataDir, selfObj): # get mainWindow object
        global APPDATA
        APPDATA = appdataDir
        self.isThreading = False
        self.selfObj = selfObj    


    def quitLauncher(self): # funcion to exit launcher
        self.selfObj.quit_button.setStyleSheet('color: gray; background-color: #fc8eac; border: 3px solid #e75480')
        if self.isThreading:
            QMessageBox.information(self.selfObj, "BSCraft Launcher", "Cannot exit, a launcher task is running.")
            self.selfObj.quit_button.setStyleSheet('color: white; background-color: #fc8eac; border: 3px solid #e75480')
        else:
            QApplication.quit()


    def invalidateFiles(self): # function to invalidate launcher files resulting in re-installation/verification of all files
        self.selfObj.reset_button.setStyleSheet('color: gray; background-color: #fc8eac; border: 3px solid #e75480')

        if self.isThreading:
            QMessageBox.information(self.selfObj, "BSCraft Launcher", "Cannot invalidate data, a launcher task is running.")
    
        else:
            promptBox = QMessageBox(parent=self.selfObj)
            promptBox.setWindowTitle("BSCraft Launcher")
            promptBox.setIcon(QMessageBox.Question)
            promptBox.setText("Are you sure that you want to invalidate launcher file cache?\n(This will make the launcher attempt to redownload all game files)")
            promptBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            promptBox.setDefaultButton(QMessageBox.No)
            promptResult = promptBox.exec_()

            if promptResult == QMessageBox.Yes:
                if os.path.isfile(APPDATA + '.bscraft/launcherValidity.json'):
                    os.remove(APPDATA + '.bscraft/launcherValidity.json')

                if os.path.isfile(APPDATA + '.bscraft/modpack/mpCVersion.json'):
                    os.remove(APPDATA + '.bscraft/modpack/mpCVersion.json')

                QMessageBox.information(self.selfObj, "BSCraft Launcher", "Invalidation success. Launcher will attempt re-install and verification of files on next game launch.")
        
        self.selfObj.reset_button.setStyleSheet('color: red; background-color: #fc8eac; border: 3px solid #e75480')

 
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
