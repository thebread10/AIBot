import discord
import json
import requests
import os
import openai
from discord.ext import commands

openai.api_key = "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"

data = {
    'guild_id': [],
    'channel_id': []
}

@bot.command()
async def export_data(ctx):
     print(data)

@bot.command()
async def import_data(ctx, json_data):
     data = json_data

@bot.command()
async def train_bot(ctx):
    trainer.train()

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
    if message.author == bot.user:
        return
    for i in data['guild_id']:
        if i == message.guild.id:
            isPresent = True
            break

    if isPresent == True: 
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=message.content
        )
        channel = bot.get_channel(data['channel_id'][data['guild_id'].index(message.guild.id)])   
        await channel.send(response['choices'][0]['text'])
    else:
        await message.channel.send("No channels set")
    await bot.process_commands(message)



bot.run("MTA2NTY1MDMzMDU5Mjg3ODcyNA.GTWMfV.zxlQ7zPKZCLnDF4qIsgzjsvF74jZJmq1bb3lkA")
