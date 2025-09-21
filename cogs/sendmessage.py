import discord
from discord.ext import commands
import dotenv
import os
import traceback
from app import Seemu
from discord import app_commands

# Load environment variables from the .env file
dotenv.load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")

class PersonalMessageBot(commands.Cog):
    def __init__(self, bot: Seemu):
        self.bot = bot
        self.authorized_user_ids = os.getenv("AUTHORIZED_USER_IDS")  # Authorized user IDs

    @app_commands.command(name="envoyermessages", description="Send a personal message to all server members.")
    async def send_personal_msg(self, interaction: discord.Interaction, message: str, link: str):
        # Check if the user is authorized
        if str(interaction.user.id) not in self.authorized_user_ids:
            await interaction.response.send_message("You do not have permission to use this command.", ephemeral=True)
            return

        # Defer the response to avoid timeout
        await interaction.response.defer(thinking=True)

        # Iterate through all members and send the private message
        for member in interaction.guild.members:
            if member.bot:
                continue  # Ignore bots
            try:
                await member.send(f"{message}\n{link}")
            except discord.Forbidden:
                print(f"Unable to send a DM to {member.display_name}. They may have disabled DMs.")
            except Exception as e:
                print(f"An error occurred while sending the DM to {member.display_name}: {e}")

        await interaction.followup.send("Messages have been sent to all members!", ephemeral=True)

# Setup function to add the Cog to the bot
async def setup(bot: Seemu):
    await bot.add_cog(PersonalMessageBot(bot))