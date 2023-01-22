import discord
import json
import requests
from discord.ext import commands

bot = commands.Bot(command_prefix = "-", intents = discord.Intents.all())

API_URL = "https://api-inference.huggingface.co/models/deepparag/Aeona"
headers = {"Authorization": f"Bearer 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"}

def query(payload):
    data = json.dumps(payload)
    response = requests.request("POST", API_URL, headers=headers, data=data)
    print(json.loads(response.content.decode("utf-8")))
    return json.loads(response.content.decode("utf-8"))

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if message.content != "":
        await message.channel.send(query(message))
    await bot.process_commands(message)

bot.run("MTA2NTY1MDMzMDU5Mjg3ODcyNA.GTWMfV.zxlQ7zPKZCLnDF4qIsgzjsvF74jZJmq1bb3lkA")
