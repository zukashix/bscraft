from discord.ext import commands
import asyncio
import requests
import re
from io import BytesIO
from PIL import Image

class Skin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # @commands.Cog.listener()
    # async def on_ready(self):
    #     # logging.info(f"User: {bot.user} (ID: {bot.user.id})")
    #     print("----------------- BOT ONLINE -----------------")
    #     print("Bot has connected to server and is online.")
    #     print(f"\nUser: {self.bot.user} (ID: {self.bot.user.id})")



    # @commands.command()
    # async def test(self, ctx: commands.Context):
    #     await ctx.send("lol")

    @commands.command()
    async def skin(self, ctx, username=None, link=None):
        

        if username==None:
            await ctx.send("Enter your Minecraft username:")
            def check(message):
                return message.author == ctx.author and message.channel == ctx.channel
            
            try:
                username_msg = await self.bot.wait_for('message', check=check, timeout=60.0)
            except asyncio.TimeoutError:
                await ctx.send(ctx.message.author.mention+" I've been waiting for a minute for you to send your username.. Did you go to buy milk or what?")
                return
            
            username = username_msg.content 
            usernameValid=False
            if len(username) >= 3 or len(username) <16:
                if re.match(r'^[a-zA-Z0-9_]+$', username):
                    usernameValid = True

            if not usernameValid:
                    await ctx.send("**Invalid Username.**\nUsername must only include characters `A-Z`, `a-z`,  `_` and must be within 3 and 16 characters.")
                    return

            
        else:
            usernameValid=False
            if len(username) >= 3 or len(username) <16:
                if re.match(r'^[a-zA-Z0-9_]+$', username):
                    usernameValid = True

            if not usernameValid:
                    await ctx.send("**Invalid Username.**\nUsername must only include characters `A-Z`, `a-z`, `_` and must be within 3 and 16 characters.")
                    return
                



        if len(ctx.message.attachments) <= 0:
            await ctx.send("Username: **"+username+"**. \nSend your Minecraft Skin:")
            def check_image(message):
                return message.author == ctx.author and message.channel == ctx.channel and \
                    len(message.attachments) > 0 and message.attachments[0].filename.lower().endswith('.png')
            
            try:
                image_msg = await self.bot.wait_for('message', check=check_image, timeout=60.0)
            except asyncio.TimeoutError:
                await ctx.send(ctx.message.author.mention+" I've been waiting for you to send your skin :skull:")
                return
        
            attachment = image_msg.attachments[0]
        else:
            attachment = ctx.message.attachments[0]
        image_url = attachment.url
        image_name = attachment.filename


        if not image_name.lower().endswith('.png'):
            await ctx.send('Invalid image format. Only PNG skins are allowed.')
            return

        response = requests.get(image_url)


        if response.status_code == 200:
            image_data = BytesIO(response.content)
            try:
                image = Image.open(image_data)
            except OSError:
                await ctx.send('Invalid image file.')
                return

            width, height = image.size
            if (width, height) != (64, 64) and (width, height) != (64, 32):
                await ctx.send('Invalid skin dimensions. Only skins with dimensions 64x64 or 64x32 are allowed.')
                return
            

        save_path = './' + username+'.png'

        with open(save_path, 'wb') as f:
            f.write(response.content)

        await ctx.send(f'Minecraft skin has been successfully linked with username: **'+username+'**')

async def setup(bot):
    await bot.add_cog(Skin(bot))