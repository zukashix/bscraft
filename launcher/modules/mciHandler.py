# Module to handle minecraft launcher actions for BSCraft Launcher
# Author: zukashix

# import modules
import minecraft_launcher_lib as mclib
import modules.backUtils as Utils

import os
import shutil
import json
from zipfile import ZipFile



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

        self.mcForgeID = self.mcVerVanilla + '-forge-' + self.mcForgeVersion.split('-')[1]

        self.modpackPath = self.minecraftDirectory + '/modpack'


    def returnModpackDir(self):
        return self.modpackPath

    
    def installJava(self): # function to install java runtime
        mclib.runtime.install_jvm_runtime(self.mcJavaVersion, self.minecraftDirectory, self.progressReport)


    def installMinecraft(self): # function to install minecraft and forge modloader
        mclib.forge.install_forge_version(self.mcForgeVersion, self.minecraftDirectory, self.progressReport, mclib.runtime.get_executable_path(self.mcJavaVersion, self.minecraftDirectory).replace('java.exe','javaw.exe'))


    def installModpack(self): # function to install bscraft modpack files (WIP)
        # check for updates / install

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
        
        # make temp dir
        if os.path.isdir(self.modpackPath + '/tmp/'):
            shutil.rmtree(self.modpackPath + '/tmp/')
        os.makedirs(self.modpackPath + '/tmp/')

        # download modpack zip
        Utils.downloadFile(self.latestModpackURL, self.modpackPath + '/tmp/modpack-tmp.zip', self.progressReport)

        # set status text
        self.progressReport["setText"]("Installing Modpack...", "lightgreen")

        # extract modpack zip
        with ZipFile(self.modpackPath + '/tmp/modpack-tmp.zip', 'r') as zip:
            zip.extractall(self.modpackPath + '/tmp/')

        # remove modpack zip post extraction
        os.remove(self.modpackPath + '/tmp/modpack-tmp.zip')

        # if updating, check for files to remove
        delData = json.load(open(self.modpackPath + '/tmp/delData.json', 'r'))
        if delData['deleteRequired']:

            for rmFile in delData["toDelete"]:
                if os.path.isfile(self.modpackPath + '/' + rmFile):
                    os.remove(self.modpackPath + '/' + rmFile)

        os.remove(self.modpackPath + '/tmp/delData.json')

        # copy modpack content to game dir
        Utils.copy_folder_contents(self.modpackPath + '/tmp/', self.modpackPath)

        # delete tmp dir
        shutil.rmtree(self.modpackPath + '/tmp/')

        # write current version info
        json.dump({"local_version": self.repoModpackVersion}, open(self.modpackPath + '/mpCVersion.json', 'w'))
    

    def getRunCMD(self): # function to obtain command needed for running the game
        launchOptions = {
            "username": self.launchUsername,
            "uuid": self.userUUID,
            "token": "",
            "executablePath": mclib.runtime.get_executable_path(self.mcJavaVersion, self.minecraftDirectory).replace('java.exe', 'javaw.exe'),
            "jvmArguments": ['-Xmx{}M'.format(self.launchMemory)],
            "launcherName": "BSCraft",
            "gameDirectory": self.modpackPath
        }

        return mclib.command.get_minecraft_command(self.mcForgeID, self.minecraftDirectory, launchOptions)
