import random

import discord
from discord.ext import commands

class Misc(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        print(f'misc cog')


    @commands.command(help="Bot will send you motivation")
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

    @commands.command(help="Shows a more detailed list of available commands.")
    async def morehelp(self, ctx):
        embed = discord.Embed(
            title="**Bot Command Guide**",
            description="Here’s how to use the bot and interact with various skill channels. Follow the steps below for each task.",
            color=discord.Color.blue()
        )

        # Browse Existing Skills
        embed.add_field(
            name=":mag_right: **Browse Existing Skills**",
            value="1. Go to #join-new-skill\n2. Use the `$available` command to list all existing skills.",
            inline=False
        )

        # Join a New Skill
        embed.add_field(
            name=":bust_in_silhouette: **Join a New Skill**",
            value="1. Go to #join-new-skill\n2. Use the `$available` command to browse existing skills\n3. Use the `$join <skill>` command to join a skill channel\n\n*Replace `<skill>` with the skill you want to join.*\n",
            inline=False
        )

        # Suggest a New Skill (make #suggest-new-skill clickable)
        embed.add_field(
            name=":bulb: **Suggest a New Skill**",
            value="1. Go to #suggest-new-skill (your channel ID for `#suggest-new-skill`)\n2. Use the `$suggest <skill>` command to suggest a new skill channel\n\n*Replace `<skill>` with the skill you want to suggest.*\n",
            inline=False
        )

        # Asking a Question
        embed.add_field(
            name=":question: **Asking a Question**",
            value="1. Make sure you're in a skill channel\n2. Use the `$ask <question>` command to ask your question\n\n*Replace `<question>` with the question you want to ask.*\n",
            inline=False
        )

        # Request a Challenge
        embed.add_field(
            name=":trophy: **Request a Challenge**",
            value="1. Make sure you're in a skill channel\n2. Use the `$new` command to request a new challenge.",
            inline=False
        )

        # Footer with additional help instructions
        embed.set_footer(text="For more details on any command, type `$help <command>`.\nYou can also type `$help <category>` for more info on a category.")

        # Send the embed message
        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Misc(bot))

