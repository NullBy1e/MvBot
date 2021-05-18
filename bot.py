from discord.ext import commands
from log import log
import config
import discord
import time
import sys

bot = commands.Bot(command_prefix="$")
bot.remove_command("help")
channel1 = 0
channel2 = 0
stop = False


@bot.event
async def on_ready():
    # *When Bot is ready it will execute the code below
    print("We have logged in as {0.user}".format(bot))
    log("INFO", "Bot has started successfully!")


@bot.command(pass_context=True)
async def check(ctx):
    # TODO: check the logs if there are any errors
    await ctx.channel.send("Bot is running")


@bot.command(pass_context=True)
async def setupChan(ctx, chan1, chan2):
    # *Assigns the channel ID to the global variables
    try:
        global channel1, channel2
        channel1 = int(get_chan_id(ctx, str(chan1)))
        channel2 = int(get_chan_id(ctx, str(chan2)))
        await ctx.channel.send("Variables set")
    except TypeError as e:
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


@commands.has_role("Admin")
@bot.command(pass_context=True)
async def mvUser(ctx, member: discord.Member, number):
    global stop
    # *Moves the user to the specified channels and number of times
    # TODO: Assign 2 to number if the parameter is not set
    voice_channel = bot.get_channel(channel1)
    voice_channel2 = bot.get_channel(channel2)
    counter = 0
    for i in range(int(number)):
        if stop:
            stop = False
            break
        print(counter)
        try:
            await discord.Member.move_to(member, voice_channel)
            print("power")
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
    print("Moving user")


def get_chan_id(ctx, given_name=None):
    # *Return the channel name
    for channel in ctx.guild.channels:
        if channel.name == given_name:
            wanted_channel_id = channel.id
            return wanted_channel_id


@commands.has_role("Admin")
@bot.command(pass_context=True)
async def exitBot(ctx, given_name=None):
    # kills all process
    log("INFO", "bot stopped from Discord channel")
    sys.exit("exit command in channel")


@commands.has_role("Admin")
@bot.command(pass_context=True)
async def stop_function(ctx, given_name=None):
    # stops function
    log("INFO", "bot stopped from Discord channel")
    global stop
    stop = True


@bot.command(pass_context=True)
async def help(ctx, commandName=None):
    if commandName != None:
        pass
    else:
        embed = discord.Embed(title="Help: ")
        embed.add_field(name="hi", value="Say hello!")
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
    await ctx.send(embed=embed)


if __name__ == "__main__":
    print("Starting Script")
    bot.run(config.get_variable_from_config("Token"))

# TODO: Use the $help commands
