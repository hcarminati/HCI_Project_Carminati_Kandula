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
        **🎉 Welcome to SkillShare! 🎉**
        
---

**🔍 Browse Existing Skills**
1. Go to **#join-new-skill** to see the available skill channels.
2. Use the **`$available`** command to list all the skills you can explore.

**🚀 Join a New Skill**
1. Go to **#join-new-skill** to find all the available skills.
2. Use the **`$available`** command to browse existing skills.
3. Use **`$join <skill>`** to join a skill channel.
    - *Replace `<skill>` with the name of the skill you want to join.*

**💡 Suggest a New Skill**
1. Go to **#suggest-new-skill** to suggest a new skill.
2. Use the **`$suggest <new-skill>`** command to propose a new skill to add to the server.
    - *Replace `<new-skill>` with the name of the skill you’d like to suggest.*

**❓ Asking a Question**
1. Make sure you're in the relevant skill channel.
2. Use the **`$ask <question>`** command to ask your question.
    - *Replace `<question>` with the question you want to ask.*

    *Example*: `!ask How do I improve my Python skills?`

**🏆 Request a Challenge**
1. Make sure you're in a skill channel.
2. Use the **`$new`** command to request a challenge related to your skill.
        

---
        
**⭐️ Show Off Your Work**
1. Head to **#showcase** to share what you've been working on!
   * This is a place to show off achievements, projects, or anything you're proud of!

**🌱 Stay Engaged & Keep Learning!**
- Don’t forget to introduce yourself in **#introductions** and chat with others!
- **Ask for help** in any skill channel – we’re here to help you grow.

**✨ Need more information?**
- Type **`$help`** to get more details on the available commands.
- Type **`$help <command>`** to get detailed info about a specific command.
- Or ask in **#general-chat** – someone will be happy to help!

---

Happy learning and have fun! 🎓
        """

        # Send the message to the selected channel
        if channel:
            await channel.send(welcome_message)
        else:
            await ctx.send("Channel not found!")


# Set up the cog
async def setup(bot):
    await bot.add_cog(Send(bot))
