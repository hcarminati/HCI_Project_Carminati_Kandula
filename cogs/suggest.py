import discord
from discord.ext import commands
import asyncio
import datetime

class Suggest(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.polls = {}

    @commands.command(name="suggest", help="Suggest a new channel.")
    async def suggest(self, ctx, *, channel_name: str):

        # Check if the category the same suggested name already exists
        existing_category = discord.utils.get(ctx.guild.categories, name=f"{channel_name}")
        if existing_category:
            existing_channels = {channel.name: channel for channel in ctx.guild.text_channels}
            existing_channel = existing_channels[f"{channel_name}-lvl-1"]
            await ctx.send(f"A channel for learning about '{channel_name}' already exists {existing_channel.mention}")
            return
        embed = discord.Embed(
            title="New Channel Suggestion",
            description=f"**Suggested Skill/Channel Name:** {channel_name}\n\n"
                        "React with 👍 to approve or 👎 to reject the suggestion. "
                        "The poll will last for 1 minute.",
            color=discord.Color.blue()
        )

        message = await ctx.send(embed=embed)
        await message.add_reaction('👍')  # Yes vote
        await message.add_reaction('👎')  # No vote

        self.polls[message.id] = {
            'channel_name': channel_name,
            'created_at': datetime.datetime.utcnow(),
            'message': message,
            'votes_yes': 0,
            'votes_no': 0,
            'total_votes': 0,
        }

        await asyncio.sleep(60)  # 60 seconds = 1 minute

        # Fetch poll results
        poll = self.polls.pop(message.id, None)
        if poll:
            # Calculate poll results
            message = await ctx.fetch_message(message.id)
            yes_percentage = (poll['votes_yes'] / poll['total_votes']) * 100 if poll['total_votes'] > 0 else 0

            # If 25% or more vote "Yes", create the channels and category
            if yes_percentage >= 25:
                guild = ctx.guild

                category = await guild.create_category(f"{poll['channel_name']}")

                await guild.create_text_channel(f"{poll['channel_name']}-lvl-1", category=category)
                await guild.create_text_channel(f"{poll['channel_name']}-lvl-2", category=category)
                await guild.create_text_channel(f"{poll['channel_name']}-lvl-3", category=category)

                await message.reply(f"Poll concluded! A new category and channels for '{poll['channel_name']}' have been created.")
            else:
                await message.reply("Poll concluded! The new channel suggestion was rejected.")

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if user.bot:
            return

        if reaction.message.id in self.polls:
            poll = self.polls[reaction.message.id]

            if reaction.emoji == '👍':
                poll['votes_yes'] += 1
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
            elif reaction.emoji == '👎':
                poll['votes_no'] -= 1

            poll['total_votes'] = poll['votes_yes'] + poll['votes_no']


async def setup(bot):
    await bot.add_cog(Suggest(bot))
