import discord
from discord.ext import commands
import os
import asyncio



intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=['bs ', 'Bs ', 'bS ', 'BS '], intents=intents)



# LOAD COGS
async def load():
    cog_count=0
    for filename in os.listdir('bot/cogs/'):
        if filename.endswith('.py'):
            cog_name = filename[:-3]  # Remove the .py extension
            cog_module = f'cogs.{cog_name}'  # Construct the module name
            await bot.load_extension(cog_module)
            print(cog_module+" imported")
            cog_count=cog_count+1

    print("----------------- "+str(cog_count)+" COGS LOADED -----------------")



#LOAD BOT
async def main():
    print("\n----------------- LOADING COGS -----------------")
    await load()

    print("\n----------------- STARTING BOT -----------------")
    print("Connecting to server...")
    await bot.start('MTEyMjgyMzU3MDY2NjU1MzQyOA.GUjQL5.xBDkw9WQDTEksE2EXenKoqx6m5BzefZAht8zmk')
    



asyncio.run(main())
