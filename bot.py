from discord.ext import commands
import discord
import json
import time

bot = commands.Bot(command_prefix="n!")
channel1 = 0
channel2 = 0


@bot.command(pass_context=True)
async def check(ctx):
    await ctx.channel.send('tests')

@bot.command(pass_contaxt=True)
async def setup(ctx, chan1, chan2):
    global channel1
    global channel2
    channel1 = int(chan1)
    channel2 = int(chan2)
    await ctx.channel.send('Vars set')

@bot.command(pass_contaxt=True)
async def listChan(ctx):
    channel = []
    for i in bot.get_all_channels():
        channel.append(i)
    await ctx.channel.send(channel)

@bot.command(pass_context=True)
async def negotiate(ctx, member: discord.Member):
    print(channel1,channel2)
    voice_channel = bot.get_channel(channel1)
    voice_channel2 = bot.get_channel(channel2)
    for i in range(100):
        await discord.Member.move_to(member, voice_channel)
        time.sleep(0.5)
        await discord.Member.move_to(member, voice_channel2)
    print('Moving user')


def readConfig(id):
    with open('config.json','r') as file:
        json_data = json.load(file)
    if id == 'Token':
        return json_data["Token"]
    else:
        raise Exception ("Can't find specified id in config")

bot.run(readConfig('Token'))
