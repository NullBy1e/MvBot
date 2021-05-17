from discord.ext import commands
from log import log
import config
import discord
import time
import sys

bot = commands.Bot(command_prefix="$")
channel1 = 0
channel2 = 0


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
    # *Moves the user to the specified channels and number of times
    # TODO: Assign 2 to number if the parameter is not set
    voice_channel = bot.get_channel(channel1)
    voice_channel2 = bot.get_channel(channel2)
    counter = 0
    for i in range(int(number)):
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
async def exit(ctx, given_name=None):
    sys.exit()

if __name__ == "__main__":
    print("Starting Script")
    bot.run(config.get_variable_from_config("Token"))

# TODO: Use the $help commands
