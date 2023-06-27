import minecraft_launcher_lib as mclib
import requests
import modules.backUtils as Utils

class MinecraftLauncher():
    def __init__(self, mainDIR, username, ram):
        repoData = requests.get("https://updater.braydenedgar.com/BSCraft/launcher_data.json", headers=Utils.headers).json()

        self.launchMemory = str(ram)
        self.launchUsername = username
        self.minecraftDirectory = mainDIR

        self.mcVerVanilla = repoData["modpackVanillaVersion"]
        self.mcForgeVersion = repoData["modpackForgeVersion"]
        self.mcJavaVersion = repoData["modpackJavaVersion"]

        self.mcForgeID = self.mcVerVanilla + '-forge-' + self.mcForgeVersion.split('-')[1]

    
    def installJava(self, progressReport):
        mclib.runtime.install_jvm_runtime(self.mcJavaVersion, self.minecraftDirectory, progressReport)

