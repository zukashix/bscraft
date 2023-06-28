# BSCraft Launcher
# Author: zukashix

# import modules
import sys
import os
import platform
import json
import traceback

from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QDesktopWidget, QMessageBox, QPushButton, QLineEdit
from PyQt5.QtGui import QPixmap, QFont, QFontDatabase
from PyQt5.QtCore import Qt, pyqtSignal, pyqtSlot, QObject

import modules.backUtils as Utils
from modules.backendHandler import LauncherActions



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


class DisplayGUI(QMainWindow):
    """class to provide GUI to bootstrapper"""
    def __init__(self): 
        # init and set variables
        super(DisplayGUI, self).__init__()
        self.actionclass = LauncherActions(APPDATA, self)
        self.exception_handler = ExceptionHandler()
        self.exception_handler.errorOccurred.connect(self.display_error)

        try:
            userData = json.load(open(APPDATA + '.bscraft/BSCUserData.json', 'r'))
            usernamePlaceholder = userData['usernamePlaceholder']
            ramPlaceholder = userData['ramPlaceholder']
        except FileNotFoundError:
            ram = Utils.getRam()
            if ram < 5000:
                ramPlaceholder = '3072'
            else:
                ramPlaceholder = '6144'

            usernamePlaceholder = ''

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

        self.reset_button = QPushButton("Reset", self)
        self.reset_button.clicked.connect(self.actionclass.invalidateFiles)
        self.reset_button.setGeometry(675, 30, 100, 50)
        self.reset_button.setFont(QFont("Minecraftia", 15))
        self.reset_button.setStyleSheet('color: red; background-color: #fc8eac; border: 3px solid #e75480')

        # set textboxes
        self.username_textbox = QLineEdit(self)
        self.username_textbox.setGeometry(475, 275, 200, 30)
        self.username_textbox.setFont(QFont("Minecraftia", 15))
        self.username_textbox.setText(usernamePlaceholder)
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
