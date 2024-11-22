import os
import typing
from pyexpat.errors import messages

import discord
import pymongo
from discord.ext import commands, tasks
from openai import OpenAI
import json


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


client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY")
)

def chat_gpt(prompt):
    response = client.chat.completions.create(
        model="gpt-4o-mini-2024-07-18",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()






class Challenge(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        print("challenge cog")
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
                    gptanswer = chat_gpt(f"[No Prose] [Output only JSON] {channel.name} challenge, 'title','description'")
                    index = gptanswer.index('{')
                    result = gptanswer[index:]
                    response = result[:result.index('}') + 1]
                    res = json.loads(response)
                    message = self.create_embed(res, count)
                    await channel.send(embed=message)

                    dict = {"_id": count, "title": res.get("title"), "description": res.get("description")}
                    challenges.insert_one(dict)
                    (database.get_collection('challenge_counter')
                    .update_one({'_id': "counter"}, {"$set": {"count": count + 1}}))
                    print(int(challenge_counter.get('count')))
                except Exception as e:
                     await channel.send(f"Oops! Looks like we don't have any content right now... Check in later!")
        print('_____')


    # @tasks.loop(seconds=3600)
    # async def challenge(self):
    #     guild = self.guild()
    #     for channel in guild.text_channels:
    #         if channel.name in db.list_database_names():
    #             database = db.get_database(channel.name)
    #             try:
    #                 challenges = database.get_collection('challenges')
    #                 challenge_counter = database.get_collection('challenge_counter').find_one({'_id': "counter"})
    #                 count = int(challenge_counter.get('count'));
    #                 print(count)
    #                 c = challenges.find_one({'_id': count})
    #                 if count > len(list(challenges.find({}))):
    #                     bad_request ="Oops! get back to us later! We're coming up with some more ideas."
    #                     print(bad_request)
    #                     await channel.send(embed=bad_request)
    #                 else:
    #                     if not c.get('completed'):
    #                         challenge_message = self.create_embed(c)
    #                         await channel.send(embed=challenge_message)
    #                         self.update_challenge(challenges, c)
    #                         # print(c.get('completed'))
    #                     (database.get_collection('challenge_counter')
    #                      .update_one({'_id': "counter"}, {"$set": {"count": count + 1}}))
    #                     print(int(challenge_counter.get('count')))
    #             except Exception as e:
    #                 await channel.send(f"Oops! Looks like we don't have any content right now... Check in later!")
    #     print("************")

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
        challenge = challenges.find_one({'': False})
        print(challenge)
        message = self.create_request_embed(challenge, ctx)

        await ctx.send(embed=message)
        self.update_challenge(challenges, challenge)


    def create_request_embed(self, challenge, ctx):
        embed = discord.Embed(
            title=f"Challenge #{challenge.get('_id')}: \n{challenge.get('title')}",
            description=f"New challenge requested by {ctx.author.mention} \n\n\n"
                        f"{challenge.get('description')}\n\n\n"
                        "To complete this challenge, send your entry along with the command "
                        "```$submit *and the # of the challenge* ```"
                        "```eg: $submit 2 ```",
            color=discord.Color.orange()
        )
        return embed

    # embed for challenges.
    def create_embed(self, challenge, counter):
        embed = discord.Embed(
            title=f"Challenge #{counter}: \n{challenge.get('title')}",
            description= f"{challenge.get('description')}\n\n\n"
                        "To complete this challenge, send your entry along with the command "
                       "```$submit *and the # of the challenge* ```\n"
                        "```eg: $submit 2 ```",
            color=discord.Color.orange()
        )
        return embed

    @commands.command()
    async def flex(self, ctx):
        await ctx.send('Tape! (but not any ordinary tape)')

    # command to submit an entry to a challenge.
    @commands.command()
    async def submit(self, ctx, submission, other_text: typing.Optional[str] = None):
        # if submission.isnumeric():

        challenge_number = int(submission)
        print(challenge_number)
        challenges = self.get_challenges(ctx.channel.name)
        c = challenges.find_one({'_id': challenge_number})
        await ctx.send(f"Congrats for completing Challenge #{c.get('_id')}\n"
                           f"{c.get('title')}\n You're doing great!")

    #resets database. used only by us
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

    #Handles when the user completes challenges...
    # and if their count of completed challenges has met the requirements to level up
    @commands.Cog.listener()
    async def on_message(self, message):
        level = message.channel.name
        if message.content.startswith('$submit'):
            author =  message.author.name
            database = db.get_database(level)
            user = database.get_collection('users').find_one({"_id": author})
            # print(user)
            count = int(user.get('completed_challenges'))
            (database.get_collection('users').update_one({"_id": author},
                                                        {"$set": {'completed_challenges': count + 1}}))
            print(f"{message.author.name} completed {count} challenges")

            if count == 1 and level[:-1] != 3:
                current_lvl = level[:-1]
                next_lvl = int(level[-1]) + 1
                role_skill_name = f"{current_lvl}{next_lvl}"
                role = discord.utils.get(message.guild.roles, name=role_skill_name)

                channel = discord.utils.get(message.guild.text_channels, name=role_skill_name)
                await self.set_channel_permissions(channel, role, True)
                await user.add_roles(role)
                await channel.send(f"{message.author.mention}, you now have access to the **{role_skill_name}** channel!")
                await channel.send(f"{user.mention} has been assigned the {role.name} role.")
            return

    async def set_channel_permissions(self, channel, role, permission):
        """Sets permissions for the given role in a specific channel."""
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