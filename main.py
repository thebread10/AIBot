import re
import long_responses as long
import negative as negative 
import dataset as dataset
import discord
from discord.ext import commands

bot = commands.Bot(command_prefix = "-", intents = discord.Intents.all())

def message_probability(user_message, recognised_words, single_response=False, required_words=[], negative_response=False, reply=[]):
    message_certainty = 0
    has_required_words = True
    is_reply = False
    # Counts how many words are present in each predefined message
    for word in user_message:
        if word in recognised_words:
            message_certainty += 1

    # Calculates the percent of recognised words in a user message
    percentage = float(message_certainty) / float(len(recognised_words))
    
    for word in reply:
        if word in user_message:
            is_reply = True
            break
    
    # Checks that the required words are in the string
    for word in required_words:
        if word not in user_message:
            has_required_words = False
            break

    # Must either have the required words, or be a single response
    if has_required_words or single_response:
        return int(percentage * 100)
    elif is_reply:
        return -1
    else:
        return 0


def check_all_messages(message):
    highest_prob_list = {}

    # Simplifies response creation / adds it to the dict
    def response(bot_response, list_of_words, single_response=False, required_words=[], negative_response=False, reply=[]):
        nonlocal highest_prob_list
        highest_prob_list[bot_response] = message_probability(message, list_of_words, single_response, required_words, negative_response, reply)

    # Responses -------------------------------------------------------------------------------------------------------
    response('Hello!', dataset.hello, single_response=True)
    response('See you!', dataset.goodbye, single_response=True)
    response('I\'m doing fine, and you?', dataset.how_asking, required_words=['how'])
    response('I\'m doing fine, and you?', ['hru', 'hry'], single_response=True)
    response('I\'m a lifeless human-type with only humanoid brain which is created artificially - A bot', dataset.who_asking, required_words=["what", "who"])
    response('You\'re welcome!', dataset.thanks, single_response=True)
    response('Aww! Thanks', dataset.grateful, single_response=True)
    response('Glad to hear. So what did you do today?', dataset.reply, single_response=True)
    response('Oh! interesting ?', dataset.routine, single_response=True)
    response('Talking with you, ig? wbu', dataset.ask, required_words=["what", "doing"])
    response('Talking with you, ig? wbu', dataset.ask, required_words=["what", "upto"])
    response('Oh what is it, is it interesting?', dataset.tasks, single_response=True, reply=['yes', 'no'])

    # Longer responses
    response(long.R_ADVICE, ['give', 'advice'], required_words=['advice'])
    response(long.R_EATING, ['what', 'do', 'you', 'eat'], required_words=['you', 'eat'])

    best_match = max(highest_prob_list, key=highest_prob_list.get)
    if highest_prob_list[best_match] == -1:
        best_match = "Oh I see"
    # print(highest_prob_list)
    # print(f'Best match = {best_match} | Score: {highest_prob_list[best_match]}')

    return long.unknown() if highest_prob_list[best_match] < 1 else best_match


# Used to get the response
def get_response(user_input):
    split_message = re.split(r'\s+|[,;?!.-]\s*', user_input.lower())
    response = check_all_messages(split_message)
    return response

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
        await message.channel.send(get_response(message.content))
    await bot.process_commands(message)

bot.run("MTA2NTY1MDMzMDU5Mjg3ODcyNA.GTWMfV.zxlQ7zPKZCLnDF4qIsgzjsvF74jZJmq1bb3lkA")
