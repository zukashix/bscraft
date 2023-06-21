import sys
import time
import os
import json
import requests
import subprocess
import platform

from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QDesktopWidget
from PyQt5.QtGui import QPixmap, QFont, QFontDatabase
from PyQt5.QtCore import Qt, QEvent

plat = platform.system().lower()
if 'win' in plat:
    APPDATA = os.getenv("APPDATA") # windows
else:
    APPDATA = os.getenv("HOME") + '/' # linux


class BackendUtilities:
    def checkInternet() -> int:
        headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0',
        }
        try:
            requests.get('https://example.com', timeout=10, headers=headers)
            try:
                requests.get('https://braxtonelmer.com', timeout=10, headers=headers)
                return 0
            except:
                return 1
        except:
            return 2

    def downloadFile(file_url, file_loc) -> bool:
        try:
            headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0',
            }
            r = requests.get(file_url, stream = True, headers=headers, verify=False)
            with open(file_loc, 'w') as ufile:
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
    
    def isInstalled(self) -> bool:
        return self.ALR_INSTALLED
    
    def startProcess(self):
        if 'win' in plat:
            args = ['start', '/B',  APPDATA + '.bscraft/launcher.exe']
        else:
            args = ['nohup', 'firefox', '&']
        
        subprocess.Popen(args)
    

class DisplayGUI(QMainWindow):
    def __init__(self):
        super(DisplayGUI, self).__init__()

        # Set window properties
        self.setWindowTitle("BSCL Updater")
        self.setWindowFlag(Qt.FramelessWindowHint)
        #self.setGeometry(0, 0, 800, 400)
        self.resize(800, 400)
        self._centerWindow()

        # Set background image
        self.background_label = QLabel(self)
        self.background_label.setGeometry(0, 0, 800, 400)
        self.background_image = QPixmap("bootstrapper/bgimg.jpg")
        self.background_label.setPixmap(self.background_image)

        # Set bscl text
        self.text_label = QLabel(self)
        self.text_label.setGeometry(40, 50, 450, 80)
        QFontDatabase.addApplicationFont("bootstrapper/mcfont.ttf")
        self.text_label.setFont(QFont("MineCrafter 3", 40))
        self.text_label.setText("BSCraft")
        self.text_label.setStyleSheet("color: white")

        # set status text
        self.text_label_2 = QLabel(self)
        self.text_label_2.setGeometry(40, 340, 350, 40)
        QFontDatabase.addApplicationFont("bootstrapper/Minecraftia.ttf")
        self.text_label_2.setFont(QFont("Minecraftia", 15))
        self.text_label_2.setText("Checking For Updates")
        self.text_label_2.setStyleSheet("color: lightgreen")

    def _centerWindow(self):
        # function to help center the window on any resolution                      
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def postDisplay(self):
        print('gui should be displayed. time 0s')
        time.sleep(5)
        print('time 5s')

    def event(self, event):
        if event.type() == QEvent.InputMethodQuery:
            self.postDisplay()
        return super(DisplayGUI, self).event(event)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DisplayGUI()
    window.show()

    sys.exit(app.exec_())
