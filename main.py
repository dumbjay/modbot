import discord, os, keep_alive, asyncio, requests
from discord.ext import tasks, commands
import time


intents = discord.Intents().all()
bot = commands.Bot(command_prefix=",", intents=intents, help_command=None)

# Optionns

oauth2 = "add oauth2 invite here"
punishment_message = "Failure to abide guidelines"
support_server = "discord.gg/yourserver"
nuked = "Successfully nuked channel
embed_colour = 0xC85050

# Tasks
@tasks.loop(seconds=5)
async def status_task():
    await bot.change_presence(
        status=discord.Status.idle,
        activity=discord.Activity(type=discord.ActivityType.watching, name="Moderation Bot
    )


# Events
@bot.event
async def on_connect():
    status_task.start()


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    await bot.process_commands(message)


@bot.event
async def on_message_edit(before, after):
    if after.author == bot.user:
        return

    await bot.process_commands(after)


@bot.event
async def on_command_error(ctx, error):
    await handleEmbed(ctx.channel, "Error", str(error), embed_colour)


@bot.event
async def on_guild_join(guild):
    for channel in guild.text_channels:
        if (
            "general" in channel.name.lower()
            or "chat" in channel.name.lower()
            or "main" in channel.name.lower()
        ):
            await channel.send(
                f"Thank you for inviting me to your server! If you require assistance, please join our support server: {support_server}"
            )


# Commands

@commands.has_permissions(administrator=True)
@bot.command(name="nuke", description="nukes the channel")
async def nuke(ctx):
  #if ctx.author.id != 818968219167096863:
  #  return 
  #else:
    await ctx.message.delete()
    await handleDoomsday(ctx.message.channel)


@commands.has_permissions(send_messages=True)
@bot.command(name="invite", description="sends the bots oauth2 link")
async def invite(ctx):
    await ctx.message.delete()
    await ctx.send(oauth2)


@commands.has_permissions(send_messages=True)
@bot.command(name="help", description="displays this embed")
async def help(ctx, arg=False):
  
    available_commands = ""
    for command in bot.commands:
        if command.description == "":
            command.description = "missing description"

        available_commands+=f"• `{command}` - {command.description}\n"

    await ctx.message.delete()
    await handleEmbed(ctx.channel, "Help", available_commands, embed_colour)


@commands.has_permissions(manage_messages=True)
@bot.command(name="purge", description="removes messages")
async def purge(ctx, limit=10):
    await ctx.message.delete()
    await ctx.channel.purge(limit=limit)

        
@commands.has_permissions(ban_members=True)
@bot.command(name="unban", description="pardon individuals")
async def unban(ctx, id: int):
    await ctx.message.delete()
    user = await bot.fetch_user(id)
    await ctx.guild.unban(user)

    notification=f"Sucessfully unbanned {user}"
    await handleEmbed(ctx.channel, "Punishment", notification, embed_colour)


@commands.has_permissions(ban_members=True)
@bot.command(name="ban", description="bans users")
async def ban(ctx, member: discord.User=None, 
reason=punishment_message):
    await ctx.message.delete()
    await ctx.guild.ban(member, reason=reason)

    notification=f"Sucessfully banned {member}"
    await handleEmbed(ctx.channel, "Punishment", notification, embed_colour)


@commands.has_permissions(kick_members=True)
@bot.command(name="kick", description="deports users")
async def kick(ctx, member: discord.User=None, reason=punishment_message):
    await ctx.message.delete()
    await ctx.guild.kick(member, reason=reason)

    notification=f"Sucessfully kicked {member}"
    await handleEmbed(ctx.channel, "Punishment", notification, embed_colour)


@commands.has_permissions(administrator=True)
@bot.command(name = "deletetheserver", description = "makes dalek lose his fucking mind")
async def deletetheserver(ctx, amount = 1000000):
    await handleEmbed(ctx.channel, "Error", "Sike you thought", embed_colour)

        
@commands.has_permissions(administrator=True)
@bot.command(name = "nickall", description = "nicks the entire server")
async def nickall(ctx, *, nick):
    await ctx.message.delete()
    for member in ctx.guild.members:
      if member.bot == False:
        try:
          await member.edit(nick=nick)
          print(member.name)
        except:
          pass


@commands.has_permissions(administrator=True)
@bot.command(name = "unnickall", description = "unnicks the entire server")
async def unnickall(ctx):
    await ctx.message.delete()
    for member in ctx.guild.members:
      if member.bot == False:
        try:
          await member.edit(nick="")
          print(member.name)
        except:
          pass

@commands.has_permissions(send_messages=True)
@bot.command(name = "ping", description = "sends the bots current ping")
async def ping(ctx):
    await ctx.message.delete()
    await handleEmbed(ctx.channel, "Ping", str(bot.latency * 1000) + "ms", embed_colour)
        
        
# Functions
async def handleDoomsday(channel):
    await channel.delete()

    channel_position = channel.position
    new_channel = await channel.clone()

    await new_channel.edit(position=channel_position, sync_permissions=True)


async def handleMute(user, time):
    muted_role = discord.utils.get(user.guild.roles, name="Muted")
    await user.add_roles(muted_role)

    await asyncio.sleep(time)
    await user.remove_roles(muted_role)


async def handleEmbed(channel, title, description, color):
    await channel.send(
        embed=discord.Embed(title=title, description=description, color=color)
    )


keep_alive.start()
bot.run(os.getenv("TOKEN"))
