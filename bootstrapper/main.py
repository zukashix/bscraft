# BSCraft Launcher Bootstrapper
# Author: zukashix


# import native modules
import traceback
import sys
import os
import json
import platform

# import third-party modules
import requests
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QDesktopWidget, QMessageBox
from PyQt5.QtGui import QPixmap, QFont, QFontDatabase
from PyQt5.QtCore import Qt, QTimer

import modules.resources

# configure primary directory as per os
plat = platform.system().lower()
if 'win' in plat:
    APPDATA = os.getenv("APPDATA").replace("\\", "/") + '/' # windows
else:
    APPDATA = os.getenv("HOME") + '/' # linux


def temp_exception_hook(exctype, value, tBack):
    errorLog1 = traceback.format_exception(exctype, value, tBack, None)
    errorLog2 = ''
    for err in errorLog1:
        errorLog2 = errorLog2 + err + ' '
    error_message = "An internal error occurred:\n\n" + errorLog2
    print(error_message)
    with open('./BSCraft_Bootstrapper_Error.txt', 'w') as logfile:
        logfile.write(error_message)


class BackendUtilities:
    """Class to group  multi-use utility functions"""
    # function that performs tasks after displaying gui
    def postDisplay(mainInit):
        timer.stop()
        mainInit.install()
        mainInit.startProcess()
        sys.exit(0)


    # function to check internet connection
    def checkInternet() -> bool:
        headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0',
        }
        try:
            requests.get('https://updater.braxtonelmer.com/', timeout=10, headers=headers)
            return True
        except:
            return False


    # function to download a file using url 
    def downloadFile(file_url, file_loc) -> bool:
        try:
            headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0',
            }
            r = requests.get(file_url, stream = True, headers=headers, verify=False)
            with open(file_loc, 'wb') as ufile:
                for chunk in r.iter_content(chunk_size=1024):
        
                # Writing one chunk at a time to file (No excessive memory usage on large-size files)
                    if chunk:
                        ufile.write(chunk)
                        ufile.flush()

            return True
        
        except:
            return False


class BackendInitiliazer():
    """Class to handle backend working of the bootstrapper"""
    def __init__(self):
        # validate if a version of launcher is already installed
        try:
            self.ALR_INSTALLED = json.load(open(APPDATA + '.bscraft/validation.json', 'r'))["bootstrapper"]["mainExecValid"]
        except (FileNotFoundError, KeyError):
            self.ALR_INSTALLED = False

        # define local variables
        self.utils = BackendUtilities
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0',
            }
    

    # function to tell if launcher is already installed
    def isInstalled(self) -> bool:
        return self.ALR_INSTALLED
    
    # function to get size of latest file in MBs
    def getMbSize(self) -> str:
        fileUrl = requests.get("https://updater.braxtonelmer.com/BSCraft/bootstrapper_data.json", headers=self.headers).json()['latest_url']
        fileByteSize = int(requests.head(fileUrl, headers=self.headers).headers['Content-Length'])
        return str(int(fileByteSize / 1048576))

    # function to start the launcher process
    def startProcess(self):
        if 'win' in plat:
            args = "start /B {}.bscraft/launcher.exe".format(APPDATA)
        else:
            args = "nohup firefox &" # for linux, dev use only. will be removed in target build
        
        os.system(args)


    # function to install the latest available version of launcher
    def install(self):
        repoData = requests.get("https://updater.braxtonelmer.com/BSCraft/bootstrapper_data.json", headers=self.headers).json()

        try:
            os.makedirs(APPDATA + '.bscraft')
        except FileExistsError:
            pass

        self.utils.downloadFile(repoData['latest_url'], APPDATA + '.bscraft/launcher.exe')

        # write json for checking validity of launcher
        validityJsonData = {
            'bootstrapper': {
                'mainExecValid': True,
                'localVersion': repoData['latest_version']
            }
        }

        json.dump(validityJsonData, open(APPDATA + '.bscraft/validation.json', 'w'))


    # function to check for launcher updates
    def checkForUpdate(self) -> bool:
        repoData = requests.get("https://updater.braxtonelmer.com/BSCraft/bootstrapper_data.json", headers=self.headers).json()
        localData = json.load(open(APPDATA + '.bscraft/validation.json', 'r'))

        if localData['bootstrapper']['localVersion'] == repoData['latest_version']:
            return False
        else:
            return True

    

class DisplayGUI(QMainWindow):
    """class to provide GUI to bootstrapper"""
    def __init__(self, mainInit): 
        # init and set variables
        super(DisplayGUI, self).__init__()

        # load external resources
        QFontDatabase.addApplicationFont(":/Minecraftia.ttf")

        # Set window properties
        self.setWindowTitle("BSCL Updater")
        self.setWindowFlag(Qt.FramelessWindowHint)
        #self.setGeometry(0, 0, 800, 400)
        self.resize(800, 450)
        self._centerWindow()

        # Set background image
        self.window_bg = QLabel(self)
        self.window_bg.setGeometry(0, 0, 800, 450)
        self.window_bg.setPixmap(QPixmap(":/bgimg.jpg"))

        # set current status text
        self.status_label = QLabel(self)
        self.status_label.setGeometry(40, 400, 350, 40)
        self.status_label.setFont(QFont("Minecraftia", 15))
        self.status_label.setText("Downloading... ({} MB)".format(mainInit.getMbSize()))
        self.status_label.setStyleSheet("color: lightgreen")


    # function to help center the window on any resolution 
    def _centerWindow(self):                     
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())



if __name__ == "__main__":
    # init required data
    sys.excepthook = temp_exception_hook
    app = QApplication(sys.argv)
    iNetC = BackendUtilities.checkInternet()
    mainInit = BackendInitiliazer()
    isInst = mainInit.isInstalled()

    ## check internet conditions and installed files

    # condition: no internet/server
    if not iNetC:
        if not isInst:
            # quit program because internet/server unavailable and launcher not installed
            QMessageBox.critical(None, "BSCraft Launcher", "No internet or server down. Quitting because files are missing.")
        else:
            # start launcher directly because no internet/server available to check for updates
            QMessageBox.warning(None, "BSCraft Launcher", "Could not check for updates. No internet or server down. Press OK to continue launching.")
            mainInit.startProcess()
            
        QApplication.quit()

    # condition: internet/server available
    else:
        if isInst:
            if not mainInit.checkForUpdate():
                mainInit.startProcess()
                sys.exit(0)


        # perform fresh install / update 
        window = DisplayGUI(mainInit) # create gui
        window.show()
        
        timer = QTimer()
        timer.timeout.connect(lambda: BackendUtilities.postDisplay(mainInit))
        timer.start(1000)

        sys.exit(app.exec_())
        
