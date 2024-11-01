import discord
from discord.ext import commands

class Ask(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="q", help="Ask the bot a question.")
    async def ask(self, ctx, *, question=None):
        if question is None:
            await ctx.send("Please ask a question after `$q`.")
        else:
            # Here, you can add functionality to respond to the question.
            await ctx.send(f"You asked: {question}")

async def setup(bot):
    await bot.add_cog(Ask(bot))
