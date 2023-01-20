import re
import torch
import discord
from transformers import AutoModelForCausalLM AutoTokenizer GPT2Tokenizer, GPT2LMHeadModel
from discord.ext import commands

bot = commands.Bot(command_prefix = "-", intents = discord.Intents.all())

tokenizer = AutoTokenizer.from_pretrained("af1tang/personaGPT")
model = AutoModelForCausalLM.from_pretrained("af1tang/personaGPT")

if torch.cuda.is_available():
    model = model.cuda

flatten = lambda l: [item for sublist in l for item in sublist]

def to_data(x):
    if torch.cuda.is_available():
        x = x.cpu()
    return x.data.numpy()

def to_var(x):
    if not torch.is_tensor(x):
        x = torch.Tensor(x)
    if torch.cuda.is_available():
        x = x.cuda()
    return x

def display_dialog_history(dialog_hx):
    for j, line in enumerate(dialog_hx):
        msg = tokenizer.decode(line)
        if j %2 == 0:
            print(">> User: "+ msg)
        else:
            print("Bot: "+msg)
            print()

def generate_next(bot_input_ids, do_sample=True, top_k=10, top_p=.92,
                  max_length=1000, pad_token=tokenizer.eos_token_id):
    full_msg = model.generate(bot_input_ids, do_sample=True,
                                              top_k=top_k, top_p=top_p, 
                                              max_length=max_length, pad_token_id=tokenizer.eos_token_id)
    msg = to_data(full_msg.detach()[0])[bot_input_ids.shape[-1]:]
    return msg

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
        bot_input_ids = to_var([flatten(dialog_hx)]).long()
        msg = generate_next(bot_input_ids)
        await message.channel.send(tokenizer.decode(msg, skip_special_tokens=True))
    await bot.process_commands(message)

bot.run("MTA2NTY1MDMzMDU5Mjg3ODcyNA.GTWMfV.zxlQ7zPKZCLnDF4qIsgzjsvF74jZJmq1bb3lkA")
