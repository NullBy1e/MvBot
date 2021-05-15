from discord.ext import commands
import discord
import json
import time

bot = commands.Bot(command_prefix = "$")
channel1 = 0
channel2 = 0


@bot.event
async def on_ready():
    #*When Bot is ready it will execute the code below
    print('We have logged in as {0.user}'.format(bot))


@bot.command(pass_context = True)
async def check(ctx):
    #TODO: check & create the logs and print if there are any errors
    await ctx.channel.send('Bot is running')


@bot.command(pass_contaxt = True)
async def setupChan(ctx, chan1, chan2):
    #*Assigns the channel ID to the global variables
    #TODO: Add try/catch and add to logs
    global channel1, channel2
    channel1 = int(get_chan_id(ctx, str(chan1)))
    channel2 = int(get_chan_id(ctx, str(chan2)))
    await ctx.channel.send('Variables set')
    print('Settings Variables: '+ str(channel1) + ';'+str(channel2))


@bot.command(pass_contaxt = True)
async def getChanId(ctx, *, given_name = None):
    #*Get channel Id and print it in the channel that the command is used in
    for channel in ctx.guild.channels:
        if channel.name == given_name:
            wanted_channel_id = channel.id
    await ctx.send(wanted_channel_id)


@commands.has_role("Admin")
@bot.command(pass_context = True)
async def mvUser(ctx, member: discord.Member, number):
    #*Moves the user to the specified channels and number of times
    #TODO: Add try/catch
    voice_channel = bot.get_channel(channel1)
    voice_channel2 = bot.get_channel(channel2)
    counter = 0
    for i in range(int(number)):
        print(counter)
        await discord.Member.move_to(member, voice_channel)
        print('power')
        counter += 1
        await discord.Member.move_to(member, voice_channel2)
        if counter == 5:
            print('Cooldown')
            time.sleep(3)
            counter = 0
    print('Moving user')


def read_config(name):
    #* Read config and return the name of variable
    with open('config.json', 'r') as file:
        json_data = json.load(file)
    if name == 'Token':
        return json_data["Token"]
    else:
        raise Exception("Can't find specified id in config")


def get_chan_id(ctx, given_name = None):
    #*Return the channel name
    for channel in ctx.guild.channels:
        if channel.name == given_name:
            wanted_channel_id = channel.id
            return wanted_channel_id


bot.run(read_config('Token'))


# TODO: Use the $help commands