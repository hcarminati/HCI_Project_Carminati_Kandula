import discord
from discord.ext import commands


class Send(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        print(f'Send cog loaded')

    @commands.command(name="send", help="Sends a welcome message to the specified channel")
    async def send(self, ctx, channel_name: str):
        print("Command triggered")

        # Get the channel by name
        channel = discord.utils.get(ctx.guild.text_channels, name=channel_name)

        # The message to send
        welcome_message = """
***Welcome to SkillShare!***

**✦ Browse Existing Skills**
1. Go to #join-new-skill
2. Use the **$available** command

**✦ Join a new Skill**
1. Go to #join-new-skill
2. Use the **$available** command to browse existing skills
3. Use the **$join <skill>** command.
        * Replace `<skill>` with the skill you want to join.

**✦ Suggest a new Skill**
1. Go to #suggest-new-skill
2. Use the **$suggest <skill>** command
        * Replace `<skill>` with the skill you want to suggest.

**✦ Asking a Question**
1. Make sure you are in a skill channel
2. Use the **$ask <question>** command
        * Replace `<question>` with the question you want to ask

**✦ Request a Challenge**
1. Make sure you are in a skill channel
2. Use the **$new** command
        """

        # Send the message to the selected channel
        if channel:
            await channel.send(welcome_message)
        else:
            await ctx.send("Channel not found!")


# Set up the cog
async def setup(bot):
    await bot.add_cog(Send(bot))
