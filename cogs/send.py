import discord
from discord.ext import commands

class Send(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        print(f'send cog')

    @commands.command(name="send", help="blah")
    async def send(self, ctx, channel_name: str, message: str):
        channel = discord.utils.get(ctx.guild.text_channels, name=channel_name)
        welcome_message = """
                Welcome to SkillShare! 
                
                - Join a new Skill
                1. Go to #join-new-skill 
                2. Use the **$join <skill>** command 

                - Browse Existing Skills 
                1. Go to #join-new-skill 
                2. Use the **$available** command 

                - Suggest a new Skill 
                1. Go to #suggest-new-skill 
                2. Use the **$suggest <skill>** command

                - Asking a Question
                1. Make sure you are in a skill channel
                2. Use the **$ask <question>** command

                - Request a Challenge 
                1. Make sure you are in a skill channel
                2. Use the **$new** command
                """
            # Send the welcome message to the current channel
        await channel.send(welcome_message)

        if channel:
            await channel.send(message)  # Send the message to the channel
            await ctx.send(f'Message sent to {channel.mention}')
        else:
            await ctx.send(f'Channel "{channel_name}" not found.')


async def setup(bot):
    await bot.add_cog(Send(bot))
