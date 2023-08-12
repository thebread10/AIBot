import discord
import json
import requests
import os
import asyncio
import time
from discord.ext import commands

bot = commands.Bot(command_prefix = "b?", intents = discord.Intents.all())

API_URL = "https://api-inference.huggingface.co/models/facebook/blenderbot-400M-distill"

def query(payload):
    headers = {"Authorization": "Bearer " + os.environ['HUGGING_FACE_TOKEN']}
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

full_msg = ''
prev_msg_user = ''

past_msg = []
responses = []

creator_array = [
    'who created you?',
    'Who created you?',
    'who create you?',
    'Who create you?',
    'who created u?',
    'who create u?',
    'Who create u?',
    'who your creator?',
    'Who your creator?',
    'Who ur creator?',
    'who ur creator?',
    'who created you',
    'Who created you',
    'who create you',
    'Who create you',
    'who created u',
    'Who created u',
    'who create u',
    'Who create u',
    'who your creator',
    'Who your creator',
    'Who ur creator',
    'who ur creator'
]

data = {
    'guild_id': [],
    'channel_id': []
}

def concatenate_message(msg, author):
    while asyncio.sleep(5):
        if prev_msg_user == author:
            full_msg += msg
            asyncio.sleep(5)
        else:
            return False

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
    for i in creator_array:
        if message.content == i:
            await message.channel.send('I was developed in BitBot Corp by user watashibaka.')
            return
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
        past_msg.append(full_msg.content)
        if len(past_msg) == 4:
            past_msg.clear()
            responses.clear()
        time.sleep(0.75)
        async with message.channel.typing():
            full_msg = message.content
            while True:
                concatenate_message(full_msg, message.author)
            data_msg = { "inputs": { "past_user_inputs": past_msg, "generated_responses": responses, "text": full_msg } }
            res = query(data_msg)  
            responses.append(res["generated_text"])
            await channel.send(res["generated_text"])
            full_msg = ''
            prev_msg_user = message.author
    await bot.process_commands(message)



bot.run(os.environ['DISCORD_TOKEN'])
