from discord.ext import commands

class Manager(commands.Cog):
    """gerencia o bot"""
    
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"READY!\nPROFILE: {self.bot.user} ")

def setup(bot):
    bot.add_cog(Manager(bot))