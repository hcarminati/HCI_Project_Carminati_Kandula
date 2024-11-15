import discord
from discord.ext import commands

class Complete(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        print(f'complete cog')


    @commands.command(name="complete", help="Complete a challenge.")
    async def complete(self, ctx, *, question=None):
        if question is None:
            await ctx.send("Please include your challenge submissions in the same message after `$complete {challenge-number}`.")
        else:
            await ctx.send(f"You submitted: {question}")

async def setup(bot):
    await bot.add_cog(Complete(bot))
