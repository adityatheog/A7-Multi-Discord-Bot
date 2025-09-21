import discord
from discord.ext import commands
import os
import json

FILE_WORDS = "forbidden_words.json"

def load_forbidden_words():
    if os.path.exists(FILE_WORDS):
        with open(FILE_WORDS, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_forbidden_words(words):
    with open(FILE_WORDS, "w", encoding="utf-8") as f:
        json.dump(words, f, indent=4)

class WordFilter(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.forbidden_words = load_forbidden_words()

    @commands.command(name="setforbiddenword")
    async def set_forbidden_word(self, ctx: commands.Context, *, word: str):
        """Add a word to the forbidden words list."""
        word = word.lower()
        self.forbidden_words[word] = True
        save_forbidden_words(self.forbidden_words)
        await ctx.send(f"✅ Forbidden word added: `{word}`")

    @commands.command(name="listforbiddenwords")
    async def list_words(self, ctx):
        if not self.forbidden_words:
            await ctx.send("🚫 No forbidden words have been set.")
        else:
            words = ", ".join(f"`{word}`" for word in self.forbidden_words)
            await ctx.send(f"📌 Current forbidden words: {words}")

    @commands.command(name="scanmessages")
    async def scan_messages(self, ctx: commands.Context, limit: int = 100):
        """Scan old messages for forbidden words."""
        if not self.forbidden_words:
            await ctx.send("❌ No forbidden words set.")
            return

        await ctx.send(f"🔍 Scanning the last **{limit}** messages...")

        deleted_count = 0

        async for message in ctx.channel.history(limit=limit):
            if message.author.bot:
                continue

            for embed in message.embeds:
                embed_content = ""

                if embed.title:
                    embed_content += embed.title + " "
                if embed.description:
                    embed_content += embed.description + " "
                if embed.footer and embed.footer.text:
                    embed_content += embed.footer.text + " "
                for field in embed.fields:
                    embed_content += field.name + " " + field.value + " "

                embed_content = embed_content.lower()

                if any(word in embed_content for word in self.forbidden_words):
                    try:
                        await message.delete()
                        deleted_count += 1
                        break
                    except Exception as e:
                        print(f"Error deleting: {e}")

        await ctx.send(f"✅ **{deleted_count}** message(s) have been deleted.")

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot or not self.forbidden_words:
            return

        for embed in message.embeds:
            embed_content = ""

            if embed.title:
                embed_content += embed.title + " "
            if embed.description:
                embed_content += embed.description + " "
            if embed.footer and embed.footer.text:
                embed_content += embed.footer.text + " "
            for field in embed.fields:
                embed_content += field.name + " " + field.value + " "

            embed_content = embed_content.lower()

            if any(word in embed_content for word in self.forbidden_words):
                try:
                    await message.delete()
                    print("🔴 Message deleted (forbidden word detected).")
                except Exception as e:
                    print(f"Error deleting: {e}")
                return

        await self.bot.process_commands(message)

async def setup(bot: commands.Bot):
    await bot.add_cog(WordFilter(bot))