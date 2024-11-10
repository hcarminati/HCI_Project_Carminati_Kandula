import discord as discord
from discord.ext import commands
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY")
)

# def chat_gpt(prompt):
#     response = client.chat.completions.create(
#         model="gpt-4o-mini-2024-07-18",
#         # model="text-embedding-3-small",
#         messages=[{"role": "user", "content": prompt}]
#     )
#     return response.choices[0].message.content.strip()

class Ask(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.requests_made = 0

    @commands.command(name="ask", help="Ask the bot a question.")
    async def ask(self, ctx, *, question=None):
        print(f"Running command 'ask' with question: {question}")

        if "-lvl-" not in ctx.channel.name:
            join_channel = discord.utils.get(ctx.guild.text_channels, name="join-new-skill")
            await ctx.send(f"You can only use the ask command in skill channels.")
            return

        if question is None:
            await ctx.send("Please include your question in the same message after `$ask`.")
            return

        username = ctx.author.name
        await ctx.send(f"{username} asked: {question}")

        # try:
        #     response = chat_gpt(question)
        #     if response is None:
        #         # If chat_gpt() returned None, that means there was an error.
        #         await ctx.send(
        #             "Something went wrong while trying to get an answer. Please try asking your question again.")
        #     else:
        #         await ctx.send(response)
        #
        # except Exception as e:
        #     # Catch any unexpected errors and inform the user
        #     await ctx.send("An unexpected error occurred. Please try again later.")
        #     print(f"Unexpected error: {e}")

async def setup(bot):
    await bot.add_cog(Ask(bot))
