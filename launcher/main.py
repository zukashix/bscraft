# BSCraft Launcher
# Author: zukashix

# Immediate exception handling block to handle unknown exceptions
try:
    import time
    # import modules
    import traceback
    import sys
    import os
    import platform
    import re
    import json

    from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QDesktopWidget, QMessageBox, QPushButton, QLineEdit
    from PyQt5.QtGui import QPixmap, QFont, QFontDatabase
    from PyQt5.QtCore import Qt, QThread, pyqtSignal
    
    import modules.backUtils as Utils
    from modules.mciHandler import MinecraftLauncher

    # configure primary directory as per os
    plat = platform.system().lower()
    if 'win' in plat:
        APPDATA = os.getenv("APPDATA").replace("\\", "/") + '/' # windows
    else:
        APPDATA = os.getenv("HOME") + '/' # linux
            

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

            try:
                self.validityData = json.load(open(APPDATA + '.bscraft/launcherValidity.json', 'r'))
            except:
                self.validityData = {
                    'javaValid': False,
                    'forgeValid': False,
                    'vanillaValid': False,
                    'modpackValid': False
                }

                json.dump(self.validityData, open(APPDATA + '.bscraft/launcherValidity.json', 'w'))
    
        def run(self):
            # ensure all variables are valid
            # validate username
            usernameValid = False

            if len(self.mcUsername) >= 3:
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


            self.Launcher = MinecraftLauncher(APPDATA + '.bscraft', self.mcUsername, self.userMemory)

            # begin installation tasks
            # install java
            if not self.validityData["javaValid"]:
                self.Launcher.installJava()
                
                self.validityData = json.load(open(APPDATA + '.bscraft/launcherValidity.json', 'r'))
                self.validityData["javaValid"] = True
                json.dump(self.validityData, open(APPDATA + '.bscraft/launcherValidity.json', 'w'))

            
            self.actionclass.isThreading = False
            self.finished.emit()
 

    class LauncherActions():
        """class to organize all actions performed by the launcher"""
        def __init__(self, selfObj): # get mainWindow object
            self.isThreading = False
            self.selfObj = selfObj    

        def quitLauncher(self): # funcion to exit launcher
            if self.isThreading:
                QMessageBox.information(self.selfObj, "BSCraft Launcher", "Cannot exit, a launcher task is running.")
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
            ram = Utils.getRam()
            if ram < 5000:
                ramPlaceholder = '3072'
            else:
                ramPlaceholder = '6144'

            # load external resources
            QFontDatabase.addApplicationFont("resources/mcfont.ttf")
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
            self.status_label.setGeometry(40, 400, 350, 40)
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
