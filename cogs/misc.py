import random

import discord
from discord.ext import commands

class Misc(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        print(f'misc cog')


    @commands.command()
    async def peptalk(self, ctx):
        affirmations = [
            "You are unstoppable. Keep pushing forward!",
            "Every step you take brings you closer to your goals.",
            "You are stronger than any challenge you face.",
            "Today is your day to shine – go after it!",
            "You have the power to make things happen.",
            "Success is not a matter of luck; it's your determination.",
            "Don't stop now – you’re closer than you think!",
            "Your potential is limitless. Keep going!",
            "You are capable of achieving amazing things.",
            "You’ve got this. One step at a time!",
            "Your dreams are within reach. Stay focused.",
            "Believe in yourself – you are your own greatest asset.",
            "The only limit is the one you set for yourself. Break through it!",
            "The harder you work, the greater the reward. Keep at it!",
            "You’re building something great. Trust the process.",
            "Keep your head up and your heart strong. You are capable.",
            "Success is earned, and you’re doing the work. Keep moving forward!",
            "No matter how tough it gets, you are tougher.",
            "Today is another opportunity to show up for yourself.",
            "You are your biggest supporter – keep lifting yourself up!"
        ]
        await ctx.send(f"{ctx.author.mention}{random.choice(affirmations)}")


async def setup(bot):
    await bot.add_cog(Misc(bot))

