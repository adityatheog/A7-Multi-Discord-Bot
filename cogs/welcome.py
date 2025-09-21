import discord
from discord.ext import commands
from discord import app_commands
import os
from app import Seemu
import json

CONFIG_FILE = "config.json"

class WelcomeBot(commands.Cog):
    def __init__(self, bot: Seemu):
        self.bot = bot

    def load_config(self):
        # Load the configuration if it exists
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, "r") as f:
                    return json.load(f)
            except json.JSONDecodeError:
                print("Error while reading the configuration file.")
                return {}
        return {}  # Return an empty dictionary if no configuration is found

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        config = self.load_config()
        welcome_channel_id = config.get("welcome_channel")
        # channel = self.bot.get_channel(1355533113022746826)  # Welcome channel ID
        if welcome_channel_id:
            channel = self.bot.get_channel(int(welcome_channel_id))
            if channel:
                embed = discord.Embed(
                    title="Oh! A new member has joined!",  # Fixed title
                    description=f"Welcome {member.mention}! 🎉",
                    color=discord.Color.green()
                )
                # Add welcome image
                embed.set_image(url="https://i.ibb.co/WWJxwhpJ/BIENVENUE-2.gif?quality=lossless")
                # Add member’s avatar as thumbnail
                embed.set_thumbnail(url=member.avatar.url)

                # Send the embed to the welcome channel
                await channel.send(embed=embed)

# Add this to configure the bot
async def setup(bot: Seemu):
    await bot.add_cog(WelcomeBot(bot))