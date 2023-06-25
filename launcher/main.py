# BSCraft Launcher
# Author: zukashix

# Immediate exception handling block to handle unknown exceptions
try:
    # import native modules
    import traceback
    import sys
    import os
    import json
    import time
    import platform # will be removed in target release
    #import subprocess
    # check if updates, retest

    # import third-party modules
    import requests
    from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QDesktopWidget, QMessageBox, QPushButton, QLineEdit
    from PyQt5.QtGui import QPixmap, QFont, QFontDatabase
    from PyQt5.QtCore import Qt, QThread, pyqtSignal

    # configure primary directory as per os
    plat = platform.system().lower()
    if 'win' in plat:
        APPDATA = os.getenv("APPDATA").replace("\\", "/") + '/' # windows
    else:
        APPDATA = os.getenv("HOME") + '/' # linux


    class BackendUtilities:
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
            

    class playGameThread(QThread):
        finished = pyqtSignal()
    
        def run(self):
            print('> playGame(0)')
            time.sleep(5)
            print('> playGame(5)')
            self.finished.emit()
 

    class LauncherActions:
        """class to organize all actions performed by the launcher"""

        def quitLauncher():
            sys.exit(0)

        def playGame(selfObj):
            selfObj.button_1.setEnabled(False)
            thread = playGameThread(parent=selfObj)
            thread.finished.connect(lambda: selfObj.button_1.setEnabled(True))
            thread.finished.connect(thread.deleteLater)
            thread.start()


    class DisplayGUI(QMainWindow):
        """class to provide GUI to bootstrapper"""
        def __init__(self): 
            # init and set variables
            super(DisplayGUI, self).__init__()

            # load external resources
            self.background_image = QPixmap("resources/bgimg.jpg")
            QFontDatabase.addApplicationFont("resources/mcfont.ttf")
            QFontDatabase.addApplicationFont("resources/Minecraftia.ttf")

            # Set window properties
            self.setWindowTitle("BSCraft Launcher")
            self.setWindowFlag(Qt.FramelessWindowHint)
            #self.setGeometry(0, 0, 800, 400)
            self.resize(800, 400)
            self._centerWindow()

            # Set background image
            self.background_label = QLabel(self)
            self.background_label.setGeometry(0, 0, 800, 400)
            self.background_label.setPixmap(self.background_image)

            # Set labels
            
            self.text_label = QLabel(self)
            self.text_label.setGeometry(40, 50, 450, 120)
            self.text_label.setFont(QFont("MineCrafter 3", 40))
            self.text_label.setText("BSCraft")
            self.text_label.setStyleSheet("color: white")

            self.text_label_2 = QLabel(self)
            self.text_label_2.setGeometry(40, 340, 350, 40)
            self.text_label_2.setFont(QFont("Minecraftia", 15))
            self.text_label_2.setText("Ready!")
            self.text_label_2.setStyleSheet("color: lightgreen")

            self.text_label_3 = QLabel(self)
            self.text_label_3.setGeometry(425, 215, 350, 40)
            self.text_label_3.setFont(QFont("Minecraftia", 15))
            self.text_label_3.setText("Username:")
            self.text_label_3.setStyleSheet("color: black")

            # set action buttons
            self.button_1 = QPushButton("Play!", self)
            self.button_1.clicked.connect(lambda: LauncherActions.playGame(self))
            self.button_1.setGeometry(400, 300, 100, 50)
            self.button_1.setFont(QFont("Minecraftia", 15))
            self.button_1.setStyleSheet('background-image: url(resources/buttons.png); border: 2px solid black')

            self.button_2 = QPushButton("Quit", self)
            self.button_2.clicked.connect(LauncherActions.quitLauncher)
            self.button_2.setGeometry(550, 300, 100, 50)
            self.button_2.setFont(QFont("Minecraftia", 15))
            self.button_2.setStyleSheet('background-image: url(resources/buttons.png); border: 2px solid black')

            # set textboxes
            self.textbox_1 = QLineEdit(self)
            self.textbox_1.setGeometry(425, 250, 200, 30)
            self.textbox_1.setFont(QFont("Minecraftia", 15))
            self.textbox_1.setStyleSheet('background-image: url(resources/buttons.png); border: 2px solid black')


        # function to help center the window on any resolution 
        def _centerWindow(self):                     
            qr = self.frameGeometry()
            cp = QDesktopWidget().availableGeometry().center()
            qr.moveCenter(cp)
            self.move(qr.topLeft())



    if __name__ == "__main__":
        # run app
        app = QApplication(sys.argv)
        window = DisplayGUI()
        window.show()
        sys.exit(app.exec_())
                

# handle unknown exceptions
except Exception as e1:
    try:
        # try to report full exception through gui
        errorLog = traceback.format_exc()
        app = QApplication(sys.argv)
        errorLog = "An internal error occurred:\n\n" + errorLog
        QMessageBox.critical(None, "BSCraft Launcher", errorLog)
        exit(1)
    except Exception as e2:
        # report minimal error to console if gui fails
        print('> Internal error. Most likely a native install or PyQt issue.')
        print(f'> E1: {e1}\n> E2: {e2}')
        exit(1)
