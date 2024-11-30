import discord
from discord.ext import commands

class Join(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        print(f'join cog')

    @commands.command(name="join", help="Join a skill channel - Usage: $join <skill_name>")
    async def join(self, ctx, *, skill_name: str):
        """Allows users to join a skill channel by skill name."""

        skill_name = skill_name.lower()
        category = discord.utils.get(ctx.guild.categories, name=skill_name)

        if not category:
            await ctx.send(f"Sorry, no such skill category '{skill_name}' exists. Please choose from the available skills.")
            return

        # find role associated with first level
        role_skill_name = f"{skill_name.lower()}-lvl-1"
        role = discord.utils.get(ctx.guild.roles, name=role_skill_name)

        # create role if it does not exist
        if not role:
            role = await ctx.guild.create_role(name=role_skill_name)

        # Check if user already has role
        # if not: add the role
        if role not in ctx.author.roles:
            await ctx.author.add_roles(role)
            await ctx.send(
                f"**{ctx.author.name}**, you have been given the {role_skill_name} role "
                f"and now have access to the **{skill_name}** channel!")
        else:
            await ctx.send(f"**{ctx.author.name}**, you already have the {role_skill_name} role.")

        # Find channel associated with skill
        channel = discord.utils.get(ctx.guild.text_channels, name=role_skill_name)

        if channel:
            # Set the channel permissions - allow user to view and send messages
            await self.set_channel_permissions(channel, role, True)
            await ctx.send(f"You now have access to the **{role_skill_name}** channel!")
        else:
            await ctx.send(f"Sorry, there is no channel for {role_skill_name} yet.")

    async def set_channel_permissions(self, channel, role, permission):
        """Sets permissions for the given role in a specific channel."""
        overwrites = {
            channel.guild.default_role: discord.PermissionOverwrite(read_messages=False),
            role: discord.PermissionOverwrite(read_messages=True, send_messages=True)
        }
        await channel.edit(overwrites=overwrites)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.channel.name != "join-new-skill":
            return

        if message.content.startswith('$') and not (message.content.startswith('join') or message.content.startswith('available')):
            await message.delete()
            return

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        """Handles command errors gracefully."""
        if ctx.command.name == "suggest" and ctx.channel.name != "suggest-new-skill":
            suggest_channel = discord.utils.get(ctx.guild.text_channels, name="suggest-new-skill")
            await ctx.send(f"You can only use the suggest command in the {suggest_channel.mention} channel.")
            return

        if isinstance(error, commands.MissingRequiredArgument):
            if error.param.name == 'channel_name':
                await ctx.send("You need to specify a skill name. Usage: `suggest <skill>` "
                               "Replace <skill> with the skill you want to suggest.")
                return

        if ctx.command.name == "join" and ctx.channel.name != "join-new-skill":
            join_channel = discord.utils.get(ctx.guild.text_channels, name="join-new-skill")
            await ctx.send(f"You can only use the $join command in the {join_channel.mention} channel.")
            return

        if isinstance(error, commands.MissingRequiredArgument):
            if error.param.name == 'skill_name':
                await ctx.send("You need to specify a skill name. Usage: `$join <skill>` "
                               "Replace <skill> with the skill you want to join.")
                return

        if isinstance(error, commands.CommandNotFound):
            await ctx.send("Sorry, I couldn't find that command. Please make sure you're using the correct command.")
            return

        else:
            print(f"Error occurred: {error}")
            await ctx.send("An unexpected error occurred. Please try again later.")

async def setup(bot):
    await bot.add_cog(Join(bot))
