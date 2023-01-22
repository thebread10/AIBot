import discord
import json
import requests
import os
from discord.ext import commands

bot = commands.Bot(command_prefix = "-", intents = discord.Intents.all())

API_URL = f"https://api-inference.huggingface.co/models/{os.getenv('MODEL_ID')}"
headers = {"Authorization": f"Bearer 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"}
data = {
    "guild_id": [],
    "channel_id": []
}
def query(payload):
    response = requests.request("POST", API_URL, headers=headers, json=payload)
    return response.json()['generated_text']

@bot.command()
async def set_channel(ctx): 
    data.guild_id.append(ctx.guild.id)
    data.channel_id.append(ctx.channel.id)

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
    for i in data.guild_id:
        if data.guild_id[i] == message.guild.id:
            isPresent = True
            break

    if isPresent == True:
        channel = bot.get_channel(data.channel_id[data.guild_id.index(message.guild.id)])
        await channel.send(query({
	    "inputs": {
		"past_user_inputs": [],
		"generated_responses": [],
		"text": message.content
            }
        }))
    await bot.process_commands(message)

bot.run("MTA2NTY1MDMzMDU5Mjg3ODcyNA.GTWMfV.zxlQ7zPKZCLnDF4qIsgzjsvF74jZJmq1bb3lkA")
