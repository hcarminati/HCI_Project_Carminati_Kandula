from discord.ext import commands
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY")
)

def chat_gpt(prompt):
    response = client.chat.completions.create(
        model="gpt-4o-mini-2024-07-18",
        # model="text-embedding-3-small",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()

class Ask(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.requests_made = 0

    @commands.command(name="ask", help="Ask the bot a question.")
    async def ask(self, ctx, *, question=None):
        if question is None:
            await ctx.send("Please include your question in the same message after `$ask`.")
            return

        await ctx.send(f"You asked: {question}")

        # response = chat_gpt(question)
        # print(response)
        # await ctx.send(response)

async def setup(bot):
    await bot.add_cog(Ask(bot))
