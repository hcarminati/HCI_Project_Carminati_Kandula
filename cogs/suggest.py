import os
import discord
import pymongo
from discord.ext import commands
import asyncio
import datetime

DB_USERNAME = os.environ.get('DISCORD_DB_USERNAME')
DB_PASSWORD = os.environ.get('DISCORD_DB_PASSWORD')

uri = f"mongodb+srv://{DB_USERNAME}:{DB_PASSWORD}@skillsharebot.5v7y9.mongodb.net/?retryWrites=true&w=majority&appName=skillsharebot"
db = pymongo.MongoClient(uri)
try:
    db.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

class Suggest(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.polls = {}
        print(f'Suggest cog loaded')

    @commands.command(name="suggest", help="Suggest a new channel. - Usage: $suggest <new-skill>")
    async def suggest(self, ctx, *, channel_name: str):
        if ctx.channel.name != "suggest-new-skill":
            suggest_channel = discord.utils.get(ctx.guild.text_channels, name="suggest-new-skill")
            await ctx.send(f"You can only use the $suggest command in the {suggest_channel.mention} channel.")
            return

        existing_channels = [channel for channel in ctx.guild.text_channels if channel.name.startswith(channel_name)]
        if existing_channels:
            existing_channels = {channel.name: channel for channel in ctx.guild.text_channels}
            existing_channel = existing_channels[f"{channel_name}-lvl-1"]
            await ctx.send(f"🔥 A channel for '{channel_name}' already exists! Check it out here: {existing_channel.mention}")
            return

        embed = discord.Embed(
            title="🚀 New Channel Suggestion!",
            description=f"**Suggested Skill/Channel Name:** {channel_name}\n\n"
                        "React with 👍 to approve or 👎 to reject the suggestion! \n"
                        "The poll will last for 1 minute ⏱️.",
            color=discord.Color.blue()
        )

        message = await ctx.send(embed=embed)
        await message.add_reaction('👍')
        await message.add_reaction('👎')

        await message.pin()

        self.polls[message.id] = {
            'channel_name': channel_name,
            'created_at': datetime.datetime.utcnow(),
            'message': message,
            'votes_yes': 0,
            'votes_no': 0,
            'total_votes': 0,
            'reactors': []  # List to track users who reacted with 👍
        }

        await asyncio.sleep(60)  # Poll duration: 60 seconds

        poll = self.polls.pop(message.id, None)
        if poll:
            message = await ctx.fetch_message(message.id)
            yes_percentage = (poll['votes_yes'] / poll['total_votes']) * 100 if poll['total_votes'] > 0 else 0
            print(yes_percentage)

            # If 25% or more vote "Yes", create the channels and category
            if yes_percentage >= 1:
                guild = ctx.guild
                print(yes_percentage)

                # Create the category for the skill
                category = await guild.create_category(f"{poll['channel_name']}")

                # Create text channels for the skill levels
                lvl_1_channel = await guild.create_text_channel(f"{poll['channel_name']}-lvl-1", category=category)
                lvl_2_channel = await guild.create_text_channel(f"{poll['channel_name']}-lvl-2", category=category)
                lvl_3_channel = await guild.create_text_channel(f"{poll['channel_name']}-lvl-3", category=category)

                # Create voice channels for the skill levels
                lvl_1_voice = await guild.create_voice_channel(f"{poll['channel_name']}-lvl-1-voice", category=category)
                lvl_2_voice = await guild.create_voice_channel(f"{poll['channel_name']}-lvl-2-voice", category=category)
                lvl_3_voice = await guild.create_voice_channel(f"{poll['channel_name']}-lvl-3-voice", category=category)

                # Create roles for the skill levels
                roles = []
                for level in ['lvl-1', 'lvl-2', 'lvl-3']:
                    role_name = f"{poll['channel_name']}-{level}"
                    role = discord.utils.get(guild.roles, name=role_name)

                    if not role:
                        role = await guild.create_role(name=role_name)
                    roles.append(role)

                # Set text channel permissions based on roles
                await self.set_channel_permissions(lvl_1_channel, roles[0])
                await self.set_channel_permissions(lvl_2_channel, roles[1])
                await self.set_channel_permissions(lvl_3_channel, roles[2])

                # Set voice channel permissions based on roles
                await self.set_voice_channel_permissions(lvl_1_voice, roles[0])
                await self.set_voice_channel_permissions(lvl_2_voice, roles[1])
                await self.set_voice_channel_permissions(lvl_3_voice, roles[2])

                self.create_databases(channel_name)

                for user_id in poll['reactors']:
                    print("user_id:", user_id)
                    user = ctx.guild.get_member(user_id)
                    print("user: ", user)
                    if user:
                        role_lvl_1 = discord.utils.get(guild.roles, name=f"{poll['channel_name']}-lvl-1")
                        print("role_lvl_1:", role_lvl_1)
                        await user.add_roles(role_lvl_1)
                        await lvl_1_channel.send(f"{user.mention} has been assigned the {role_lvl_1.name} role.")

                await message.reply(
                    f"🎉 Poll concluded! A new category and channels for '{poll['channel_name']}' have been created.")
            else:
                await message.reply("🚫 Poll concluded! The new channel suggestion was rejected.")

            await message.unpin()

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if user.bot:
            return

        if reaction.message.id in self.polls:
            poll = self.polls[reaction.message.id]

            if reaction.emoji == '👍':
                poll['votes_yes'] += 1
                if user.id not in poll['reactors']:
                    poll['reactors'].append(user.id)
            elif reaction.emoji == '👎':
                poll['votes_no'] += 1

            poll['total_votes'] = poll['votes_yes'] + poll['votes_no']

    @commands.Cog.listener()
    async def on_reaction_remove(self, reaction, user):
        if user.bot:
            return

        if reaction.message.id in self.polls:
            poll = self.polls[reaction.message.id]

            if reaction.emoji == '👍':
                poll['votes_yes'] -= 1
                if user.id in poll['reactors']:
                    poll['reactors'].remove(user.id)
            elif reaction.emoji == '👎':
                poll['votes_no'] -= 1

            poll['total_votes'] = poll['votes_yes'] + poll['votes_no']

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.channel.name != "suggest-new-skill":
            return

        if message.content.startswith('$') and not message.content.startswith('$suggest'):
            await message.delete()
            await message.channel.send(
                f"Oops! 🚫 {message.author.mention}, you can only use the `$suggest` command in this channel.")
            return

    async def set_channel_permissions(self, channel, role):
        """Sets the permissions for the given text channel to allow only the specific role to access it."""
        overwrites = {
            channel.guild.default_role: discord.PermissionOverwrite(read_messages=False),
            role: discord.PermissionOverwrite(read_messages=True, send_messages=True)
        }
        await channel.edit(overwrites=overwrites)

    async def set_voice_channel_permissions(self, voice_channel, role):
        """Sets the permissions for the given voice channel to allow only the specific role to join."""
        overwrites = {
            voice_channel.guild.default_role: discord.PermissionOverwrite(connect=False),
            role: discord.PermissionOverwrite(connect=True)
        }

        try:
            await voice_channel.edit(overwrites=overwrites)
        except discord.DiscordException as e:
            print(f"Error setting permissions for {voice_channel.name}: {e}")

    def create_databases(self, name):
        database_lvl1 = db[f"{name}-lvl-1"]
        database_lvl1.create_collection("challenges")
        database_lvl1.create_collection("challenge_counter")
        database_lvl1.get_collection("challenge_counter").insert_one({'_id': "counter", 'count': 0})
        database_lvl1.create_collection("users")


        database_lvl2 = db[f"{name}-lvl-2"]
        database_lvl2.create_collection("challenges")
        database_lvl2.create_collection("challenge_counter")
        database_lvl2.get_collection("challenge_counter").insert_one({'_id': "counter", 'count': 0})
        database_lvl2.create_collection("users")

        database_lvl3 = db[f"{name}-lvl-3"]
        database_lvl3.create_collection("challenges")
        database_lvl3.create_collection("challenge_counter")
        database_lvl3.get_collection("challenge_counter").insert_one({'_id': "counter", 'count': 0})
        database_lvl3.create_collection("users")


async def setup(bot):
    await bot.add_cog(Suggest(bot))
