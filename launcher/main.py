# BSCraft Launcher
# Author: zukashix

# Immediate exception handling block to handle unknown exceptions
try:
    # import native modules
    import traceback
    import sys
    import os
    import platform

    # import third-party modules
    from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QDesktopWidget, QMessageBox, QPushButton, QLineEdit
    from PyQt5.QtGui import QPixmap, QFont, QFontDatabase
    from PyQt5.QtCore import Qt, QThread, pyqtSignal

    # configure primary directory as per os
    plat = platform.system().lower()
    if 'win' in plat:
        APPDATA = os.getenv("APPDATA").replace("\\", "/") + '/' # windows
    else:
        APPDATA = os.getenv("HOME") + '/' # linux
            

    class playGameThread(QThread):
        finished = pyqtSignal()
        def __init__(self, username, ram, actionclass, parent=None):
            super(playGameThread, self).__init__()
            self.mcUsername = username
            self.userMemory = ram
            self.actionclass = actionclass
    
        def run(self):
            # ensure all variables are correct
            print(self.mcUsername)
            print(self.userMemory)

            #minecraft = MinecraftLauncher(APPDATA + '.bscraft/', 'zukashix', '200')
            
            self.actionclass.isThreading = False
            self.finished.emit()
 

    class LauncherActions():
        """class to organize all actions performed by the launcher"""
        def __init__(self, selfObj):
            self.isThreading = False
            self.selfObj = selfObj    

        def quitLauncher(self):
            if self.isThreading:
                QMessageBox.information(self.selfObj, "BSCraft Launcher", "Cannot exit, a launcher task is running.")
            else:
                QApplication.quit()

        def _deleteThread(self):
            if self.thread is not None:
                self.thread.finished.disconnect(self._deleteThread)
                self.thread.deleteLater()
                self.thread = None

        def playGame(self, username, ram):
            self.selfObj.play_button.setEnabled(False)
            self.isThreading = True
            self.thread = playGameThread(username, ram, self, parent=self.selfObj)
            self.thread.finished.connect(lambda: self.selfObj.play_button.setEnabled(True))
            self.thread.finished.connect(self._deleteThread)
            self.thread.start()



    class DisplayGUI(QMainWindow):
        """class to provide GUI to bootstrapper"""
        def __init__(self): 
            # init and set variables
            super(DisplayGUI, self).__init__()
            self.actionclass = LauncherActions(self)

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
            self.username_textbox.setText("Player0")
            self.username_textbox.setStyleSheet('color: white; background-color: #fc8eac; border: 3px solid #e75480')

            self.ram_textbox = QLineEdit(self)
            self.ram_textbox.setGeometry(475, 200, 200, 30)
            self.ram_textbox.setFont(QFont("Minecraftia", 15))
            self.ram_textbox.setText("4096")
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
