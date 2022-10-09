import os
from decouple import config
from discord.ext import commands
import discord

TOKEN = config("TOKEN_SECRET")
#intents = discord.Intents.default()
#intents = discord.Intents.all()
#intents.members = True

bot = commands.Bot(command_prefix = "!", intents = discord.Intents.all())

# bot = commands.Bot("!") -> Todos os comandos do bot terão o prefixo !

def load_cogs(bot):
    bot.load_extension("manager")
    bot.load_extension("tasks.weatherInformation")
    for file in os.listdir("commands"):
        if file.endswith(".py"):
            cog = file[:-3]
            bot.load_extension(f"commands.{cog}")

load_cogs(bot)

bot.run(TOKEN)