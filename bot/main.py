import discord
import os
#import pynacl
#import dnspython
import server
from discord.ext import commands
from mzcr import dispDigest
import traceback

bot = commands.Bot(command_prefix="!")
TOKEN = os.getenv("DISCORD_TOKEN")


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}({bot.user.id})")


def multiline_code_block(text):
    return "```" + text + "```"


@bot.command()
async def ping(ctx):
    try:
        await ctx.send(multiline_code_block(dispDigest()))
    except:
        await ctx.send(multiline_code_block(traceback.format_exc()))

server.server()
bot.run(TOKEN)
