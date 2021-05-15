from discord.ext import commands
from discord.guild import Guild
import discord
import json
import time

bot = commands.Bot(command_prefix="$")
channel1 = 0
channel2 = 0


@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))


@bot.command(pass_context=True)
async def check(ctx):
    await ctx.channel.send('Bot is running')


@bot.command(pass_contaxt=True)
async def setupChan(ctx, chan1, chan2):
    global channel1
    global channel2
    channel1 = int(getChanID(ctx, str(chan1)))
    channel2 = int(getChanID(ctx, str(chan2)))
    await ctx.channel.send('Variables set')


@bot.command(pass_contaxt=True)
async def getChan(ctx, *, given_name=None):
    for channel in ctx.guild.channels:
        if channel.name == given_name:
            wanted_channel_id = channel.id
    await ctx.send(wanted_channel_id)  # this is just to check


@commands.has_role("Admin")
@bot.command(pass_context=True)
async def mvUser(ctx, member: discord.Member, number):
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


def readConfig(name):
    with open('config.json', 'r') as file:
        json_data = json.load(file)
    if name == 'Token':
        return json_data["Token"]
    else:
        raise Exception("Can't find specified id in config")


def getChanID(ctx, given_name=None):
    for channel in ctx.guild.channels:
        if channel.name == given_name:
            wanted_channel_id = channel.id
            return wanted_channel_id


bot.run(readConfig('Token'))
