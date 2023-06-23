# BSCraft Launcher Bootstrapper
# Author: zukashix

# Immediate exception handling block to handle unknown exceptions
try:
    # import native modules
    import traceback
    import sys
    import os
    import json
    import platform # will be removed in target release

    # import third-party modules
    import requests
    from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QDesktopWidget, QMessageBox
    from PyQt5.QtGui import QPixmap, QFont, QFontDatabase
    from PyQt5.QtCore import Qt, QEvent, QTimer

    # configure primary directory as per os
    plat = platform.system().lower()
    if 'win' in plat:
        APPDATA = os.getenv("APPDATA").replace("\\", "/") + '/' # windows
    else:
        APPDATA = os.getenv("HOME") + '/' # linux


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
                args = "nohup firefox" # for linux, dev use only. will be removed in target build
            
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
        def __init__(self, statusText): # a min okay hey can you open the ftp server here 
            # init and set variables
            super(DisplayGUI, self).__init__()
            self.statusText = statusText

            # Set window properties
            self.setWindowTitle("BSCL Updater")
            self.setWindowFlag(Qt.FramelessWindowHint)
            #self.setGeometry(0, 0, 800, 400)
            self.resize(800, 400)
            self._centerWindow()

            # Set background image
            self.background_label = QLabel(self)
            self.background_label.setGeometry(0, 0, 800, 400)
            self.background_image = QPixmap("./bootstrapper/resources/bgimg.jpg")
            self.background_label.setPixmap(self.background_image)

            # Set text for logo 
            
            self.text_label = QLabel(self)
            self.text_label.setGeometry(40, 50, 450, 120)
            QFontDatabase.addApplicationFont("./bootstrapper/resources/mcfont.ttf")
            self.text_label.setFont(QFont("MineCrafter 3", 40))
            self.text_label.setText("BSCraft")
            self.text_label.setStyleSheet("color: white")

            # set current status text
            self.text_label_2 = QLabel(self)
            self.text_label_2.setGeometry(40, 340, 350, 40)
            QFontDatabase.addApplicationFont("./bootstrapper/resources/Minecraftia.ttf")
            self.text_label_2.setFont(QFont("Minecraftia", 15))
            self.text_label_2.setText(self.statusText)
            self.text_label_2.setStyleSheet("color: lightgreen")


        # function to help center the window on any resolution 
        def _centerWindow(self):                     
            qr = self.frameGeometry()
            cp = QDesktopWidget().availableGeometry().center()
            qr.moveCenter(cp)
            self.move(qr.topLeft())



    if __name__ == "__main__":
        # init required data
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
                sys.exit(1)
            else:
                # start launcher directly because no internet/server available to check for updates
                QMessageBox.warning(None, "BSCraft Launcher", "Could not check for updates. No internet or server down. Press OK to continue launching.")
                mainInit.startProcess()
                sys.exit(0) 

        # condition: internet/server available
        else:
            if isInst:
                # check for updates if launcher already installed
                if mainInit.checkForUpdate():
                    filesize = mainInit.getMbSize() # get update filesize
                    statustext = "Updating... ({} MB)".format(filesize)

                    window = DisplayGUI(statustext) # create gui
                    window.show()

                    timer = QTimer()
                    timer.timeout.connect(lambda: BackendUtilities.postDisplay(mainInit))
                    timer.start(1000)
                    
                    sys.exit(app.exec_())

                mainInit.startProcess() # start launcher and exit bootstrapper
                exit(0)

            else: # if launcher not installed, perform fresh install
                filesize = mainInit.getMbSize() # get install filesize
                statustext = "Installing... ({} MB)".format(filesize)

                window = DisplayGUI(statustext) # create gui
                window.show()
                
                timer = QTimer()
                timer.timeout.connect(lambda: BackendUtilities.postDisplay(mainInit))
                timer.start(1000)

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
