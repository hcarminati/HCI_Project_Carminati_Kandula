import asyncio
import discord
from discord.ext import commands

class Available(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="available", help="List all available skill channels or search by skill name.")
    async def available(self, ctx, search: str = None):
        """Lists all the available skill categories and their levels or search for specific skills."""
        if ctx.channel.name != "suggest-new-skill":
            join_channel = discord.utils.get(ctx.guild.text_channels, name="join-new-skill")
            await ctx.send(f"You can only use the join command in the {join_channel.mention} channel.")
            return

        categories = sorted(ctx.guild.categories, key=lambda category: category.name.lower())

        available_skills = []

        for category in categories:
            skill_channels = [channel.name for channel in category.text_channels if "lvl-" in channel.name]

            if skill_channels:
                available_skills.append({
                    "category": category.name,
                    "channels": skill_channels
                })

        if not available_skills:
            await ctx.send("No available skills to join at the moment.")
            return

        if search:
            search = search.lower()

            filtered_skills = []
            for skill in available_skills:
                matching_channels = [channel for channel in skill["channels"] if search in channel.lower()]
                if search in skill["category"].lower() or matching_channels:
                    filtered_skills.append({
                        "category": skill["category"],
                        "channels": matching_channels if matching_channels else skill["channels"]
                    })

            if not filtered_skills:
                await ctx.send(f"No skills found matching '{search}'. Please try a different query.")
                return

            available_skills = filtered_skills

        # Pagination
        per_page = 10
        total_pages = (len(available_skills) // per_page) + (1 if len(available_skills) % per_page else 0)

        def create_embed(page_number):
            start = (page_number - 1) * per_page
            end = start + per_page
            page_skills = available_skills[start:end]

            embed = discord.Embed(
                title="Available Skills to Join",
                description="Join any skill by using $join <skill_name>.\n\n"
                            "Search for a skill by providing a keyword after the command. "
                            "For example: `!available coding`.\n",
                color=discord.Color.green()
            )

            for skill in page_skills:
                embed.add_field(name=f'- {skill["category"]}', value='', inline=False)

            embed.set_footer(text=f"Page {page_number}/{total_pages}")

            return embed

        embed = create_embed(1)

        message = await ctx.send(embed=embed)

        await message.add_reaction("⬅️")
        await message.add_reaction("➡️")

        # Reaction handling
        def check(reaction, user):
            return user != self.bot.user and str(reaction.emoji) in ["⬅️", "➡️"] and reaction.message.id == message.id

        current_page = 1

        while True:
            try:
                reaction, user = await self.bot.wait_for('reaction_add', timeout=60.0, check=check)

                if str(reaction.emoji) == "⬅️" and current_page > 1:
                    current_page -= 1
                elif str(reaction.emoji) == "➡️" and current_page < total_pages:
                    current_page += 1

                embed = create_embed(current_page)
                await message.edit(embed=embed)

                await message.remove_reaction(reaction, user)

            except asyncio.TimeoutError:
                await message.clear_reactions()
                break

async def setup(bot):
    await bot.add_cog(Available(bot))
