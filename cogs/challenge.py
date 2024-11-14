import discord
from discord.ext import commands, tasks
import pymongo
import os

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
        self.challenge.start()
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
                challenges = database.get_collection('challenges')
                challenge_counter = database.get_collection('challenge_counter').find_one({'_id': "counter"})
                count = int(challenge_counter.get('count'));
                c = challenges.find_one({'_id': count})

                if count > len(list(challenges.find({}))):
                    badrequest ="Oops! get back to us later! We're coming up with some more ideas."
                    print(badrequest)
                    await channel.send(badrequest)
                else:
                    if not c.get('completed'):
                        challengeMessage = f'Challenge #{c.get("_id")} \n {c.get("title")} \n {c.get("description")}'
                        await channel.send(challengeMessage)
                        challenges.update_one({"_id": c.get("_id")}, {"$set": {'completed': True}})
                    (database.get_collection('challenge_counter')
                     .update_one({'_id': "counter"}, {"$set": { "count": count + 1 }}))
        print("************")


    @commands.command()
    async def ping(self, ctx):
        await ctx.send('Pong!')




async def setup(bot):
    print("cog setup")
    await bot.add_cog(Challenge(bot))