import discord
from discord.ext import commands
import json


help_Json = json.load(open("commands.json", "r"))


def get_help_msg(name):
    returned_values = []
    if name == "All":
        for x in help_Json:
            description = help_Json[x]["description"]
            returned_values.append(description)
    else:
        for x in help_Json:
            if x == name:
                description = help_Json[x]["description"]
                returned_values.append(description)
    return returned_values


def get_help_args(name):
    returned_values = []
    if name == "All":
        for x in help_Json:
            args = help_Json[x]["args"]
            returned_values.append(args)
    else:
        for x in help_Json:
            if x == name:
                args = help_Json[x]["args"]
                returned_values.append(args)
    return returned_values


def get_help_name(name):
    returned_values = []
    if name == "All":
        for x in help_Json:
            returned_values.append(x)
    else:
        for x in help_Json:
            if x == name:
                returned_values.append(x)
    return returned_values
