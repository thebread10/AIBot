import discord
import json
import requests
import os
from discord.ext import commands

bot = commands.Bot(command_prefix = "L?", intents = discord.Intents.all())

API_URL = "https://8dbe55d1-e280-4579-9d33-277428e35ecd.deepnoteproject.com/model/ai-gen/work"

def query(payload):
    headers = { "Content-type" : "application/json" }
    response = requests.post(API_URL, headers=headers, json=payload)
    print(response)
    return response

data = {
    'guild_id': [],
    'channel_id': []
}

@bot.command()
async def export_data(ctx):
     print(data)
     ctx.message.delete()

@bot.command()
async def import_data(ctx, json_data):
     data = json_data
     ctx.message.delete()

@bot.command()
async def set_channel(ctx):
    isGuild = True
    for i in data['guild_id']:
        if i == ctx.guild.id:
            isGuild = False
    if isGuild == True:
        data['guild_id'].append(ctx.guild.id)
        data['channel_id'].append(ctx.channel.id)
        await ctx.send("Channel Set Successfully, Enjoy")
    else:
        await ctx.send("Guild already registered")

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.event
async def on_message(message):
    isPresent = False
    isChannel = False
    if message.author == bot.user:
        return
    for i in data['guild_id']:
        if i == message.guild.id:
            isPresent = True
            break
    for i in data['channel_id']:
        if i == message.channel.id:
            isChannel = True
            break

    if isPresent == True and isChannel == True:
        channel = bot.get_channel(data['channel_id'][data['guild_id'].index(message.guild.id)])
        data_msg = { "inputs": { "text": message.content } }
        await channel.send(query(data_msg))
    await bot.process_commands(message)



bot.run("MTA2NTY1MDMzMDU5Mjg3ODcyNA.GTWMfV.zxlQ7zPKZCLnDF4qIsgzjsvF74jZJmq1bb3lkA")
