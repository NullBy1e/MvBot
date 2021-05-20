import discord
from discord.ext import commands


"""
    Nazwa komendy; funkcja
    Nazwe params
"""


__helpMsgs__ = {"default": "test", "setupChan": "Sets up the channels", "userinfo": ""}


def get_help_msg(name):
    print(name)
    if name == "All":
        for x in __helpMsgs__:
            finalMsgs = []
            finalMsgs.append(x)
            return finalMsgs
    if name in __helpMsgs__:
        return __helpMsgs__.get(name)
