import sys
import time
import os
import json
import requests

from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QDesktopWidget
from PyQt5.QtGui import QPixmap, QFont, QFontDatabase
from PyQt5.QtCore import Qt, QEvent


#APPDATA = os.getenv("APPDATA") # windows
APPDATA = os.getenv("HOME") + '/' # linux


class BackendUtilities:
    def checkInternet() -> int:
        try:
            requests.get('https://example.com', timeout=10)
            try:
                requests.get('https://braxtonelmer.com', timeout=10)
                return 0
            except (requests.ConnectionError, requests.Timeout):
                return 1
        except (requests.ConnectionError, requests.Timeout):
            return 2
        
    


class BackendInitiliazer():
    def __init__(self):
        try:
            self.ALR_INSTALLED = json.load(open(APPDATA + '.bscraft/validation.json', 'r'))["bootstrapper"]["mainExecValid"]
        except (FileNotFoundError, KeyError):
            self.ALR_INSTALLED = False
    
    def isInstalled(self) -> bool:
        return self.ALR_INSTALLED
    

        

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

        # Set initial text
        self.text_label = QLabel(self)
        self.text_label.setGeometry(40, 50, 350, 40)
        QFontDatabase.addApplicationFont("bootstrapper/mcfont.ttf")
        self.text_label.setFont(QFont("MineCrafter 3", 15))
        self.text_label.setText("Checking for updates")
        self.text_label.setStyleSheet("color: white")

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
