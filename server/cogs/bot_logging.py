from discord.ext import commands
import discord

class Bot_Logging(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("\n----------------- BOT ONLINE -----------------")
        print("Bot has connected to server and is online.")
        print(f"\nUser: {self.bot.user} (ID: {self.bot.user.id})")



    @commands.command()
    async def ping(self, ctx: commands.Context):
        await ctx.send("pong {0}".format(round(self.bot.latency, 1)*1000))


    @commands.command()
    @commands.is_owner()
    async def die(self, ctx: commands.Context):
        await ctx.send("im ded :skull:")
        exit()

    @die.error
    async def on_application_command_error(self, ctx: commands.Context, error: discord.DiscordException):
        if isinstance(error, commands.NotOwner):
            await ctx.send("how dareth thee tryeth to kill me??")
        else:
            raise error  # Here we raise other errors to ensure they aren't ignored



    # @commands.command()
    # async def test(self, ctx: commands.Context):
    #     await ctx.send("lol")

async def setup(bot):
    await bot.add_cog(Bot_Logging(bot))