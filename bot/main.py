import discord
import os
#import pynacl
#import dnspython
import server
from discord.ext import commands
from mzcr import dispDigest

bot = commands.Bot(command_prefix="!")
TOKEN = os.getenv("DISCORD_TOKEN")


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}({bot.user.id})")


@bot.command()
async def ping(ctx):
    await ctx.send("```" + dispDigest() + "```")

server.server()
bot.run(TOKEN)
