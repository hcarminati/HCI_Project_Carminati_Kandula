import os
from pprint import pprint

import discord
import pymongo
from discord.ext import commands, tasks

GUILD = os.getenv('DISCORD_GUILD')
DB_USERNAME = os.environ.get('DISCORD_DB_USERNAME')
DB_PASSWORD = os.environ.get('DISCORD_DB_PASSWORD')

uri = f"mongodb+srv://{DB_USERNAME}:{DB_PASSWORD}@skillsharebot.5v7y9.mongodb.net/?retryWrites=true&w=majority&appName=skillsharebot"
db = pymongo.MongoClient(uri)
try:
    db.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

class Challenge(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        print("cog initialized")
        # self.init_users()

        # self.challenge.start()
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~")



    def guild(self):
        for guild in self.bot.guilds:
            if guild.name == GUILD:
                return guild
            else:
                print(guild.name)

    @tasks.loop(seconds=3600)
    async def challenge(self):
        guild = self.guild()
        for channel in guild.text_channels:
            if channel.name in db.list_database_names():
                database = db.get_database(channel.name)
                try:
                    challenges = database.get_collection('challenges')
                    challenge_counter = database.get_collection('challenge_counter').find_one({'_id': "counter"})
                    count = int(challenge_counter.get('count'));
                    print(count)
                    c = challenges.find_one({'_id': count})
                    if count > len(list(challenges.find({}))):
                        bad_request ="Oops! get back to us later! We're coming up with some more ideas."
                        print(bad_request)
                        await channel.send(embed=bad_request)
                    else:
                        if not c.get('completed'):
                            challenge_message = self.create_embed(c)
                            await channel.send(embed=challenge_message)
                            self.update_challenge(challenges, c)
                            # print(c.get('completed'))
                        (database.get_collection('challenge_counter')
                         .update_one({'_id': "counter"}, {"$set": {"count": count + 1}}))
                        print(int(challenge_counter.get('count')))
                except Exception as e:
                    await channel.send(f"Oops! Looks like we don't have any content right now... Check in later!")
        print("************")

    # helper function to update the challenge counter
    @staticmethod
    def update_counter(database, count):

        print(database.get_collection('challenge_counter').find_one({'_id': "counter"}))
        print(database)

    # helper function to update the challenge completion status
    @staticmethod
    def update_challenge(challenges, c):
        challenges.update_one({"_id": c.get("_id")}, {"$set": {'completed': True}})

    def get_challenges(self, name):
        database = db.get_database(name)
        print(database)
        challenges = database.get_collection('challenges')
        print(challenges)
        return challenges


# Command for if users choose to accept a new challenge.
    @commands.command()
    async def new(self, ctx):
        if ctx.channel.name == "join-new-skill" or ctx.channel.name == "suggest-new-skill":
            await ctx.send(
                f"{ctx.author.mention}, you can not use the $challenge command in this channel."
            )
        db_name = ctx.channel.name
        print(db_name)
        challenges = db.get_database(db_name).get_collection('challenges')
        challenge = challenges.find_one({'completed': False})
        print(challenge)
        message = self.create_request_embed(challenge, ctx)

        await ctx.send(embed=message)
        self.update_challenge(challenges, challenge)


    def create_request_embed(self, challenge, ctx):
        embed = discord.Embed(
            title=f"Challenge #{challenge.get('_id')}: \n{challenge.get('title')}",
            description=f"New challenge requested by {ctx.author.mention} \n\n\n"
                        f"{challenge.get('description')}\n\n\n"
                        "The challenge will be open for 1 week.",
            color=discord.Color.orange()
        )
        return embed

    def create_embed(self, challenge,):
        embed = discord.Embed(
            title=f"Challenge #{challenge.get('_id')}: \n{challenge.get('title')}",
            description= f"{challenge.get('description')}\n\n\n"
                        "The challenge will be open for 1 week.",
            color=discord.Color.orange()
        )
        return embed

    @commands.command()
    async def flex(self, ctx):
        await ctx.send('Tape! (but not any ordinary tape)')

    @commands.command()
    async def submit(self, ctx, submission):
        if submission.isnumeric():
            challenge_number = int(submission)
            challenges = self.get_challenges(ctx.channel.name)
            c = challenges.find_one({'_id': challenge_number})
            await ctx.send(f"Congrats for completing Challenge #{c.get('_id')}\n"
                           f"{c.get('title')}\n You're doing great!")

    def init_users(self):
        guild = self.guild()
        for channel in guild.text_channels:
            members = channel.members
            for member in members:
                database = db.get_database(channel.name)
                collection = database.get_collection('users')
                collection.insert_one({
                    '_id': member.name,
                    'completed_challenges': 0,
                })


    @commands.Cog.listener()
    async def on_message(self, message):
        if message.content.startswith('$submit'):
            database = db.get_database(message.channel.name)
            user = database.get_collection('users').find_one({"_id": message.author.name})
            print(user)
            completed_count = int(user.get('completed_challenges'))
            (database.get_collection('users').update_one({"_id": message.author.name},
                                                        {"$set": {'completed_challenges': completed_count + 1}}))
            print(completed_count)

            if (completed_count > 3):
                print("f")
            return


    async def set_channel_permissions(self, channel, role, permission):
        """Sets permissions for the given role in a specific channel.
            - Deny @everyone
            - Allow specific role
        """
        overwrites = {
            channel.guild.default_role: discord.PermissionOverwrite(read_messages=False),
            role: discord.PermissionOverwrite(read_messages=True, send_messages=True)
        }
        await channel.edit(overwrites=overwrites)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = member.guild.system_channel
        if channel is not None:
            database = db.get_database(channel.name)
            collection = database.get_collection('users')
            collection.insert_one({
                '_id': member.name,
                'completed_challenges': 0
            })
            await channel.send(f'Welcome {member.mention}!')



async def setup(bot):
    print("cog setup")
    await bot.add_cog(Challenge(bot))