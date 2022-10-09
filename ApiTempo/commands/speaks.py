from discord.ext import commands

class Speaks(commands.Cog):
    """Conversa com o usuário"""
    
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="ola")
    async def hello_bot(self, ctx):

        response = f"Olá {ctx.author.name}, Estou funcionando normalmente."

        await ctx.send(response)


def setup(bot):
    bot.add_cog(Speaks(bot))