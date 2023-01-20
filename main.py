import re
import torch
import discord
from transformers import AutoModelWithLMHead, AutoTokenizer
from discord.ext import commands

bot = commands.Bot(command_prefix = "-", intents = discord.Intents.all())

tokenizer = AutoTokenizer.from_pretrained("deepparag/Aeona")
model = AutoModelWithLMHead.from_pretrained("deepparag/Aeona")

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
        new_user_input_ids = tokenizer.encode(message + tokenizer.eos_token, return_tensors='pt')
        bot_input_ids = torch.cat([chat_history_ids, new_user_input_ids], dim=-1) if step > 0 else new_user_input_ids
        chat_history_ids = model.generate(
          bot_input_ids, max_length=200,
          pad_token_id=tokenizer.eos_token_id,  
          no_repeat_ngram_size=4,       
          do_sample=True, 
          top_k=100, 
          top_p=0.7,
          temperature=0.8
        )
        await message.channel.send(tokenizer.decode(chat_history_ids[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True))
    await bot.process_commands(message)

bot.run("MTA2NTY1MDMzMDU5Mjg3ODcyNA.GTWMfV.zxlQ7zPKZCLnDF4qIsgzjsvF74jZJmq1bb3lkA")
