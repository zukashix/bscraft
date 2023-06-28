import minecraft_launcher_lib as mclib
import requests
import modules.backUtils as Utils

import os
import shutil
import time

class MinecraftLauncher():
    def __init__(self, mainDIR, username, ram, progressReport):
        repoData = requests.get("https://updater.braydenedgar.com/BSCraft/launcher_data.json", headers=Utils.headers).json()
        self.userUUID = str(requests.get("http://tools.glowingmines.eu/convertor/nick/" + username).json()['offlinesplitteduuid'])

        self.launchMemory = str(ram)
        self.launchUsername = username
        self.minecraftDirectory = mainDIR
        self.progressReport = progressReport

        self.mcVerVanilla = repoData["modpackVanillaVersion"]
        self.mcForgeVersion = repoData["modpackForgeVersion"]
        self.mcJavaVersion = repoData["modpackJavaVersion"]

        self.mcForgeID = self.mcVerVanilla + '-forge-' + self.mcForgeVersion.split('-')[1]
        self.javaPath = 'java'

        self.modpackPath = self.minecraftDirectory + '/modpack'

    
    def installJava(self):
        mclib.runtime.install_jvm_runtime(self.mcJavaVersion, self.minecraftDirectory, self.progressReport)


    def installMinecraft(self):
        mclib.forge.install_forge_version(self.mcForgeVersion, self.minecraftDirectory, self.progressReport, self.javaPath)


    def installModpack(self):
        try:
            os.makedirs(self.modpackPath)
        except FileExistsError:
            shutil.rmtree(self.modpackPath)
            os.makedirs(self.modpackPath)

        print('[>] Simulating modpack installation by sleeping for 5s.')
        time.sleep(5)

    
    def getRunCMD(self):
        launchOptions = {
            "username": self.launchUsername,
            "uuid": self.userUUID,
            "token": "",
            "executablePath": mclib.runtime.get_executable_path(self.mcJavaVersion, self.minecraftDirectory),
            "jvmArguments": ['-Xmx{}M'.format(self.launchMemory)],
            "launcherName": "BSCraft",
            "gameDirectory": self.modpackPath
        }

        return mclib.command.get_minecraft_command(self.mcForgeID, self.minecraftDirectory, launchOptions)
