import sys
import os
import json
import requests
import subprocess
import platform

from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QDesktopWidget, QMessageBox
from PyQt5.QtGui import QPixmap, QFont, QFontDatabase
from PyQt5.QtCore import Qt, QEvent

plat = platform.system().lower()
if 'win' in plat:
    APPDATA = os.getenv("APPDATA").replace("\\", "/") + '/' # windows
else:
    APPDATA = os.getenv("HOME") + '/' # linux


class BackendUtilities:
    def checkInternet() -> bool:
        headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0',
        }
        try:
            requests.get('https://updater.braxtonelmer.com/', timeout=10, headers=headers)
            return True
        except:
            return False


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
    def __init__(self):
        try:
            self.ALR_INSTALLED = json.load(open(APPDATA + '.bscraft/validation.json', 'r'))["bootstrapper"]["mainExecValid"]
        except (FileNotFoundError, KeyError):
            self.ALR_INSTALLED = False

        self.utils = BackendUtilities
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0',
            }
    

    def isInstalled(self) -> bool:
        return self.ALR_INSTALLED
    

    def getMbSize(self) -> str:
        fileUrl = requests.get("https://updater.braxtonelmer.com/BSCraft/bootstrapper_data.json", headers=self.headers).json()['latest_url']
        fileByteSize = int(requests.head(fileUrl, headers=self.headers).headers['Content-Length'])
        return str(int(fileByteSize / 1048576))

    def startProcess(self):
        if 'win' in plat:
            args = ['start', '/B',  APPDATA + '.bscraft/launcher.exe']
        else:
            args = ['nohup', 'firefox']
        
        subprocess.Popen(args)


    def install(self):
        repoData = requests.get("https://updater.braxtonelmer.com/BSCraft/bootstrapper_data.json", headers=self.headers).json()

        try:
            os.makedirs(APPDATA + '.bscraft')
        except FileExistsError:
            pass

        self.utils.downloadFile(repoData['latest_url'], APPDATA + '.bscraft/launcher.exe')

        validityJsonData = {
            'bootstrapper': {
                'mainExecValid': True,
                'localVersion': repoData['latest_version']
            }
        }

        json.dump(validityJsonData, open(APPDATA + '.bscraft/validation.json', 'w'))


    def checkForUpdate(self) -> bool:
        repoData = requests.get("https://updater.braxtonelmer.com/BSCraft/bootstrapper_data.json", headers=self.headers).json()
        localData = json.load(open(APPDATA + '.bscraft/validation.json', 'r'))

        if localData['bootstrapper']['localVersion'] == repoData['latest_version']:
            return False
        else:
            return True

    

class DisplayGUI(QMainWindow):
    def __init__(self, statusText: str, mainInit: BackendInitiliazer):
        super(DisplayGUI, self).__init__()
        self.statusText = statusText
        self.mainInit = mainInit

        # Set window properties
        self.setWindowTitle("BSCL Updater")
        self.setWindowFlag(Qt.FramelessWindowHint)
        #self.setGeometry(0, 0, 800, 400)
        self.resize(800, 400)
        self._centerWindow()

        # Set background image
        self.background_label = QLabel(self)
        self.background_label.setGeometry(0, 0, 800, 400)
        self.background_image = QPixmap("bootstrapper/resources/bgimg.jpg")
        self.background_label.setPixmap(self.background_image)

        # Set bscl text
        self.text_label = QLabel(self)
        self.text_label.setGeometry(40, 50, 450, 80)
        QFontDatabase.addApplicationFont("bootstrapper/resources/mcfont.ttf")
        self.text_label.setFont(QFont("MineCrafter 3", 40))
        self.text_label.setText("BSCraft")
        self.text_label.setStyleSheet("color: white")

        # set status text
        self.text_label_2 = QLabel(self)
        self.text_label_2.setGeometry(40, 340, 350, 40)
        QFontDatabase.addApplicationFont("bootstrapper/resources/Minecraftia.ttf")
        self.text_label_2.setFont(QFont("Minecraftia", 15))
        self.text_label_2.setText(self.statusText)
        self.text_label_2.setStyleSheet("color: lightgreen")


    def _centerWindow(self):
        # function to help center the window on any resolution                      
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


    def postDisplay(self):
        self.mainInit.install()
        self.mainInit.startProcess()
        exit(0)


    def event(self, event):
        if event.type() == QEvent.InputMethodQuery:
            self.postDisplay()
        return super(DisplayGUI, self).event(event)


if __name__ == "__main__":
    # init required data
    app = QApplication(sys.argv)
    iNetC = BackendUtilities.checkInternet()
    mainInit = BackendInitiliazer()
    isInst = mainInit.isInstalled()
    
    # check internet conditions and installed files
    if not iNetC:
        if not isInst:
            QMessageBox.critical(None, "BSCraft Launcher", "No internet or server down. Quitting because files are missing.")
            sys.exit(1)
        else:
            QMessageBox.warning(None, "BSCraft Launcher", "Could not check for updates. No internet or server down. Press OK to continue launching.")
            mainInit.startProcess()
            sys.exit(0) 

    else:
        if isInst:
            if mainInit.checkForUpdate():
                filesize = mainInit.getMbSize()
                statustext = "Updating... ({} MB)".format(filesize)

                window = DisplayGUI(statustext, mainInit)
                window.show()
                sys.exit(app.exec_())

            mainInit.startProcess()
            exit(0)

        else:
            filesize = mainInit.getMbSize()
            statustext = "Installing... ({} MB)".format(filesize)

            window = DisplayGUI(statustext, mainInit)
            window.show()
            sys.exit(app.exec_())
            
