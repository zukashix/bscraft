# Module to handle minecraft launcher actions for BSCraft Launcher
# Author: zukashix

# import modules
import minecraft_launcher_lib as mclib
import modules.backUtils as Utils
from ftplib import FTP

import os
import shutil
import json
from zipfile import ZipFile

DLSZ = 0
LASTPERCT = 0

class MinecraftLauncher():
    """class that contains functions to interact with minecraft launcher api"""
    def __init__(self, mainDIR, username, ram, progressReport, repoData):
        # init required variables
        self.userUUID = Utils.generate_offline_uuid(username)
        self.launchMemory = str(ram)
        self.launchUsername = username
        self.minecraftDirectory = mainDIR
        self.progressReport = progressReport

        self.mcVerVanilla = repoData["modpackVanillaVersion"]
        self.mcForgeVersion = repoData["modpackForgeVersion"]
        self.mcJavaVersion = repoData["modpackJavaVersion"]

        self.repoModpackVersion = repoData["modpackLatestVersion"]
        self.latestModpackURL = repoData["modpackLatestURL"]
        self.javaURL = repoData["modpackJavaURL"]
        self.javaID = repoData["modpackJavaID"]

        self.mcForgeID = self.mcVerVanilla + '-forge-' + self.mcForgeVersion.split('-')[1]

        self.modpackPath = self.minecraftDirectory + '/modpack'

    def _dirInit(self, dir):
        if os.path.isdir(self.minecraftDirectory + f'/{dir}/'):
            shutil.rmtree(self.minecraftDirectory + f'/{dir}/')
        os.makedirs(self.minecraftDirectory + f'/{dir}/')


    def returnModpackDir(self):
        return self.modpackPath
    

    def returnJavaPath(self):
        return self.minecraftDirectory + '/runtime/' + self.javaID + '/bin/javaw.exe'

    
    def installJava(self): # function to install java runtime
        # mclib.runtime.install_jvm_runtime(self.mcJavaVersion, self.minecraftDirectory, self.progressReport)
        self._dirInit('tmp')
        self._dirInit('runtime')

        if os.path.isfile(self.minecraftDirectory + '/javaVersion.json'):
            mpLocalData = json.load(open(self.minecraftDirectory + '/javaVersion.json', 'r'))
            if mpLocalData['local_id'] == self.javaID:
                return

        # Make validity false
        validityData = json.load(open(self.minecraftDirectory + '/launcherValidity.json', 'r'))
        validityData["javaValid"] = False
        json.dump(validityData, open(self.minecraftDirectory + '/launcherValidity.json', 'w'))

        # download java zip
        Utils.downloadFile(self.javaURL, self.minecraftDirectory + '/tmp/java-tmp.zip', self.progressReport)

        # set status text
        self.progressReport["setText"]("Installing Java...", "lightgreen")

        # extract java zip
        with ZipFile(self.minecraftDirectory + '/tmp/java-tmp.zip', 'r') as zip:
            zip.extractall(self.minecraftDirectory + '/tmp/')

        os.remove(self.minecraftDirectory + '/tmp/java-tmp.zip')

        # copy java content to game dir
        Utils.copy_folder_contents(self.minecraftDirectory + '/tmp/', self.minecraftDirectory + '/runtime/')

        # delete tmp dir
        shutil.rmtree(self.minecraftDirectory + '/tmp/')

        json.dump({"local_id": self.javaID}, open(self.minecraftDirectory + '/javaVersion.json', 'w'))


    def installMinecraft(self): # function to install minecraft and forge modloader
        # mclib.forge.install_forge_version(self.mcForgeVersion, self.minecraftDirectory, self.progressReport, mclib.runtime.get_executable_path(self.mcJavaVersion, self.minecraftDirectory).replace('java.exe','javaw.exe'))
        mclib.forge.install_forge_version(self.mcForgeVersion, self.minecraftDirectory, self.progressReport, self.returnJavaPath())


    def installModpack(self): # function to install bscraft modpack files (WIP)
        # check for updates / install
        self._dirInit('tmp')

        if os.path.isfile(self.modpackPath + '/mpCVersion.json'):
            mpLocalData = json.load(open(self.modpackPath + '/mpCVersion.json', 'r'))
            if mpLocalData['local_version'] == self.repoModpackVersion:
                return
            
        if not os.path.isdir(self.modpackPath):
            os.makedirs(self.modpackPath)

        # Make validity false
        validityData = json.load(open(self.minecraftDirectory + '/launcherValidity.json', 'r'))
        validityData["modpackValid"] = False
        json.dump(validityData, open(self.minecraftDirectory + '/launcherValidity.json', 'w'))

        # download modpack zip
        Utils.downloadFile(self.latestModpackURL, self.minecraftDirectory + '/tmp/modpack-tmp.zip', self.progressReport)

        # set status text
        self.progressReport["setText"]("Installing Modpack...", "lightgreen")

        # extract modpack zip
        with ZipFile(self.minecraftDirectory + '/tmp/modpack-tmp.zip', 'r') as zip:
            zip.extractall(self.minecraftDirectory + '/tmp/')

        # remove modpack zip post extraction
        os.remove(self.minecraftDirectory + '/tmp/modpack-tmp.zip')

        # if updating, check for files to remove
        delData = json.load(open(self.minecraftDirectory + '/tmp/delData.json', 'r'))
        if delData['deleteRequired']:

            for rmFile in delData["toDelete"]:
                if os.path.isfile(self.modpackPath + '/' + rmFile):
                    os.remove(self.modpackPath + '/' + rmFile)

        os.remove(self.minecraftDirectory + '/tmp/delData.json')

        # copy modpack content to game dir
        Utils.copy_folder_contents(self.minecraftDirectory + '/tmp/', self.modpackPath)

        # delete tmp dir
        shutil.rmtree(self.minecraftDirectory + '/tmp/')

        # write current version info
        json.dump({"local_version": self.repoModpackVersion}, open(self.modpackPath + '/mpCVersion.json', 'w'))
    

    def getRunCMD(self): # function to obtain command needed for running the game
        launchOptions = {
            "username": self.launchUsername,
            "uuid": self.userUUID,
            "token": "",
            # "executablePath": mclib.runtime.get_executable_path(self.mcJavaVersion, self.minecraftDirectory).replace('java.exe', 'javaw.exe'),
            "executablePath": self.returnJavaPath(),
            "jvmArguments": ['-Xmx{}M'.format(self.launchMemory)],
            "launcherName": "BSCraft",
            "gameDirectory": self.modpackPath
        }

        return mclib.command.get_minecraft_command(self.mcForgeID, self.minecraftDirectory, launchOptions)
