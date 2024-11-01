import discord
from discord.ext import commands

class Ask(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="ask", help="Ask the bot a question.")
    async def ask(self, ctx, *, question=None):
        if question is None:
            await ctx.send("Please include your question in the same message after `$ask`.")
        else:
            await ctx.send(f"You asked: {question}")

async def setup(bot):
    await bot.add_cog(Ask(bot))
