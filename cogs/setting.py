import discord
from discord.ext import commands
import json
import os
from app import Seemu

CONFIG_FILE = "config.json"  # Configuration file to store welcome and goodbye channels


class SettingBot(commands.Cog):
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

    def save_config(self, config):
        # Save the configuration into a JSON file
        with open(CONFIG_FILE, "w") as f:
            json.dump(config, f, indent=4)

    @commands.command(name="setWelcomeChannel", help="Set the welcome channel")
    async def set_welcome_channel(self, ctx, channel: discord.TextChannel):
        config = self.load_config()

        if not channel.permissions_for(ctx.guild.me).send_messages:
            await ctx.send("I do not have permission to send messages in this channel.")
            return

        # Save the welcome channel ID in the configuration file
        config['welcome_channel'] = str(channel.id)
        self.save_config(config)

        await ctx.send(f"Welcome channel set: {channel.mention}")

    @commands.command(name="setGoodbyeChannel", help="Set the goodbye channel")
    async def set_goodbye_channel(self, ctx, channel: discord.TextChannel):
        config = self.load_config()

        if not channel.permissions_for(ctx.guild.me).send_messages:
            await ctx.send("I do not have permission to send messages in this channel.")
            return

        # Save the goodbye channel ID in the configuration file
        config['goodbye_channel'] = str(channel.id)
        self.save_config(config)

        await ctx.send(f"Goodbye channel set: {channel.mention}")


# Add this command to configure the bot
async def setup(bot: Seemu):
    await bot.add_cog(SettingBot(bot))