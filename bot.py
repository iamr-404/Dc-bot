# bot.py
import os
import discord
from discord import app_commands
from discord.ext import commands

# intents
intents = discord.Intents.default()
intents.message_content = False  # Slash commands-only bot

# Client setup
class MyBot(discord.Client):
    def __init__(self):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def on_ready(self):
        await self.tree.sync()  # Sync commands globally (or server-scoped)
        print(f"Bot is ready as {self.user}")

client = MyBot()

# ==========================
# Slash Commands start here
# ==========================

# /ping
@client.tree.command(name="ping", description="Check bot latency")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message(f"Pong! Latency: {round(client.latency*1000)}ms")

# /hello
@client.tree.command(name="hello", description="Say hello to the bot")
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message(f"Hi {interaction.user.mention}! I'm your slash bot.")

# /userinfo
@client.tree.command(name="userinfo", description="Get info about a user")
@app_commands.describe(user="Select a user")
async def userinfo(interaction: discord.Interaction, user: discord.Member):
    embed = discord.Embed(title=f"{user.name}'s Info", color=discord.Color.green())
    embed.add_field(name="Username", value=user.name)
    embed.add_field(name="ID", value=user.id)
    embed.add_field(name="Joined at", value=user.joined_at.strftime("%Y-%m-%d"))
    embed.set_thumbnail(url=user.display_avatar.url)
    await interaction.response.send_message(embed=embed)

# /serverinfo
@client.tree.command(name="serverinfo", description="Get server information")
async def serverinfo(interaction: discord.Interaction):
    guild = interaction.guild
    embed = discord.Embed(title=f"{guild.name} Info", color=discord.Color.blue())
    embed.add_field(name="Server Name", value=guild.name)
    embed.add_field(name="Server ID", value=guild.id)
    embed.add_field(name="Members", value=guild.member_count)
    embed.set_thumbnail(url=guild.icon.url if guild.icon else "")
    await interaction.response.send_message(embed=embed)

# /say
@client.tree.command(name="say", description="Make the bot say something")
@app_commands.describe(message="The message to say")
async def say(interaction: discord.Interaction, message: str):
    await interaction.response.send_message(message)

# /embed
@client.tree.command(name="embed", description="Send a custom embed")
@app_commands.describe(title="Embed title", description="Embed description")
async def embed(interaction: discord.Interaction, title: str, description: str):
    embed = discord.Embed(title=title, description=description, color=discord.Color.random())
    await interaction.response.send_message(embed=embed)

# /kick (requires permissions)
@client.tree.command(name="kick", description="Kick a member from the server")
@app_commands.describe(user="Member to kick", reason="Reason for kick")
async def kick(interaction: discord.Interaction, user: discord.Member, reason: str = "No reason provided"):
    if not interaction.user.guild_permissions.kick_members:
        await interaction.response.send_message("You don't have permission to kick members.", ephemeral=True)
        return
    try:
        await user.kick(reason=reason)
        await interaction.response.send_message(f"{user.name} has been kicked for: {reason}")
    except Exception as e:
        await interaction.response.send_message(f"Failed to kick: {e}")

# /ban (requires permissions)
@client.tree.command(name="ban", description="Ban a member from the server")
@app_commands.describe(user="Member to ban", reason="Reason for ban")
async def ban(interaction: discord.Interaction, user: discord.Member, reason: str = "No reason provided"):
    if not interaction.user.guild_permissions.ban_members:
        await interaction.response.send_message("You don't have permission to ban members.", ephemeral=True)
        return
    try:
        await user.ban(reason=reason)
        await interaction.response.send_message(f"{user.name} has been banned for: {reason}")
    except Exception as e:
        await interaction.response.send_message(f"Failed to ban: {e}")

# ==========================
# Run bot
# ==========================
TOKEN = os.getenv("TOKEN")  # Must be set in Railway or local .env
client.run(TOKEN)
