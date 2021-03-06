from discord.ext import commands
from log import log
import helpCmd
import config
import discord
import time

bot = commands.Bot(command_prefix="$")
bot.remove_command("help")
channel1 = 0
channel2 = 0
stop = False


@bot.event
async def on_ready():
    print("Logged in as {0.user}".format(bot))
    log("INFO", "Bot has started successfully!")


@bot.command(pass_context=True)
async def check(ctx):
    info = (
        " \nChannel1: "
        + str(channel1)
        + "\nChannel2: "
        + str(channel2)
        + "\nRunning on: "
        + str(bot.user)
        + "\nStop = "
        + str(stop)
    )
    await ctx.channel.send("Bot is running")
    await ctx.channel.send("Info: " + info)


@bot.command(pass_context=True)
async def setupChan(ctx, chan1, chan2):
    # *Assigns the channel ID to the global variables
    try:
        global channel1, channel2
        channel1 = int(get_chan_id(ctx, str(chan1)))
        channel2 = int(get_chan_id(ctx, str(chan2)))
        await ctx.channel.send("Variables set")
    except TypeError:
        await ctx.channel.send("Wrong Channel Names")
        log("ERROR", "Wrong Channel Name")
    except:
        log("ERROR", "Error in the setupChan function")
        await ctx.channel.send("Other error valve plz fix")
    print("Settings Variables: " + str(channel1) + ";" + str(channel2))


@bot.command(pass_context=True)
async def getChanId(ctx, *, given_name=None):
    # *Get channel Id and print it in the channel that the command is used in
    for channel in ctx.guild.channels:
        if channel.name == given_name:
            wanted_channel_id = channel.id
    await ctx.send(wanted_channel_id)


@commands.has_permissions(administrator=True)
@bot.command(pass_context=True)
async def mvUser(ctx, member: discord.Member, number=2):
    global stop, channel1, channel2
    # * Moves the user to the specified channels and number of times
    # TODO: Check if the channel 1 & 2 are None then print error message to channel
    if channel1 and channel2:
        pass
    voice_channel = bot.get_channel(channel1)
    voice_channel2 = bot.get_channel(channel2)
    counter = 0
    for _ in range(int(number)):
        if stop:
            stop = False
            break
        try:
            await discord.Member.move_to(member, voice_channel)
            counter += 1
            await discord.Member.move_to(member, voice_channel2)
            if counter == 5:
                print("Cooldown")
                time.sleep(3)
                counter = 0
        except:
            await ctx.channel.send("User is not in channel")
            log("ERROR", "User is not in channel")
            break
    print("Done Moving User")


def get_chan_id(ctx, given_name=None):
    # *Return the channel name
    for channel in ctx.guild.channels:
        if channel.name == given_name:
            wanted_channel_id = channel.id
            return wanted_channel_id


@commands.has_permissions(administrator=True)
@bot.command(pass_context=True)
async def stop_bot(ctx, given_name=None):
    log("INFO", "bot stopped from Discord channel")
    global stop
    stop = True


@bot.command(pass_context=True)
async def help(ctx, commandName=None):
    if commandName != None:
        message = helpCmd.get_help_msg(commandName)
        args = helpCmd.get_help_args(commandName)
        name = helpCmd.get_help_name(commandName)
        embed = discord.Embed(title="Help: ")
        embed.add_field(name=name[0], value=message[0])
        embed.add_field(name="Args", value=args[0])
        await ctx.send(embed=embed)
    else:
        messages = helpCmd.get_help_msg("All")
        embed = discord.Embed(title="Help")
        name = helpCmd.get_help_name("All")
        for x in range(len(name)):
            embed.add_field(name=name[x], value=messages[x])
        await ctx.message.delete()
        await ctx.send(embed=embed)


@bot.command()
async def userinfo(ctx, member: discord.Member):
    user = member
    embed = discord.Embed(
        title="USER INFO",
        description=f"Here is the info we retrieved about {user}",
        colour=user.colour,
    )
    embed.set_thumbnail(url=user.avatar_url)
    embed.add_field(name="NAME", value=user.name, inline=True)
    embed.add_field(name="NICKNAME", value=user.nick, inline=True)
    embed.add_field(name="ID", value=user.id, inline=True)
    embed.add_field(name="STATUS", value=user.status, inline=True)
    embed.add_field(name="TOP ROLE", value=user.top_role.name, inline=True)
    embed.add_field(
        name="Account Created",
        value=user.created_at.__format__("%A, %d. %B %Y @ %H:%M:%S"),
    )
    embed.add_field(
        name="Join Date", value=user.joined_at.__format__("%A, %d. %B %Y @ %H:%M:%S")
    )
    await ctx.send(embed=embed)


@bot.command(pass_context=True)
async def getGuildId(ctx):
    id = ctx.message.guild.id
    await ctx.channel.send(id)


@bot.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def defaults(ctx, action, variable_name=None, variable=None):
    if action == "read":
        serverId = ctx.message.guild.id
        var = config.get_variable_from_config(serverId)
        if var:
            await ctx.channel.send(var)
        else:
            await ctx.channel.send("*Cant find anything in config*")
    elif action == "write":
        serverId = ctx.message.guild.id
        if variable_name and variable:
            config.write_variable_to_config(
                serverId, {str(variable_name): str(variable)}
            )
            await ctx.channel.send("Done!")
    elif action == "delete":
        serverId = ctx.message.guild.id
        if variable_name:
            config.delete_variable_to_config(serverId, variable_name)
            await ctx.channel.send("Done!")
    else:
        await ctx.channel.send("Can't find specified action")


@bot.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def text(ctx, *argv):
    await ctx.message.delete()
    message = ""
    for x in argv:
        message += " "
        message += str(x)
    await ctx.channel.send(message)


@bot.command(pass_context=True)
async def dm(ctx, message, member: discord.Member):
    user = member
    await user.send(message)


@bot.command(pass_context=True, no_pm=True)
async def avatar(ctx, member: discord.Member):
    await ctx.send("{}".format(member.avatar_url))


if __name__ == "__main__":
    bot.run(config.get_variable_from_config("Token"))
