import discord
import os
import wolframalpha
import io
import aiohttp
import json
import ast

def load_history():
    return get_history(100, False)

def add_to_history(question, answer):

    question_history.append(str(question))
    answer_history.append(str(answer))

def get_history(lenght = 100, flip = True):
    with open("history.json", 'r') as history_file:
        content = history_file.read()
        history_list = ast.literal_eval(content)
        if len(history_list[0]) < lenght or len(history_list[0]) < lenght:
            lenght = len(history_list[0])
        if flip:
            history_list[0] = history_list[0][::-1]
            history_list[1] = history_list[1][::-1]
        history_list[0] = history_list[0][:lenght:]
        history_list[1] = history_list[1][:lenght:]
        return history_list

def save_history(history_list):
    with open("history.json", 'w') as history_file:
        history_file.write(str(history_list))

def clear_history():
    empty_history = [[],[]]
    history_list[0].clear()
    history_list[1].clear()
    save_history(empty_history)


def mixed_form_translator(bf):
    list = bf.split("(")
    list2 = list[1].split("/")
    fn = int(list[0])*int(list2[1])
    rft = fn+ int(list2[0])
    rfn = list2[1]
    rf = "("+str(rft)+"/"+str(rfn)+")"
    return rf


def find_end_p_index(start, string):
    counter = 1
    for endi in range(start, len(string)):
        if (string[endi] == '('):
            counter += 1
        if (string[endi] == ')'):
            counter -= 1
            if counter == 0:
                return endi
    return -1

def reformat_question(question):
    while "bf" in question:
        start = question.index("bf")
        replacestring = (mixed_form_translator(question[start +2:find_end_p_index(start + 4, question)]))
        sub1 = question[:start]
        sub2 = question[find_end_p_index(start + 4, question)+1:]
        question = sub1 + replacestring + sub2
    return question

def reformat_answer(answer):
    newanswer = ""
    for x in range(len(answer[0])):
        newanswer += "Question: " + str(answer[0][x])+"\nAnswer: " + str(answer[1][x])+"\n"
    return newanswer


def wolfram_text_answer(question):
    res = client_wolfram.query(question)
    return next(res.results).text


keys = open('keys.txt', 'r').read()
keylist = keys.split(",")

helptext = "use format !wolfram <question> in standard wolfram format to get text answer \nuse format !imagewolfram <question> in standard wolfram format to get full image answer\nuse format bf<num>(<num>/<num>) to use mixed form"

client = discord.Client()
app_id_wolfram = keylist[0]
client_wolfram = wolframalpha.Client(app_id_wolfram)

history_list = load_history()
question_history = history_list[0]
answer_history = history_list[1]
 
@client.event
async def on_ready():
   print('We have logged in as {0.user}'.format(client))
 
@client.event
async def on_message(message):
   if message.author == client.user:
       return
   if message.content.startswith('!wolframhistory'):
       answer = get_history()
       answer = reformat_answer(answer)
       await message.channel.send(answer)
    
   elif message.content.startswith('!wolframclearhistory'):
      clear_history()
      await message.channel.send("Successfully cleared!")
        
   elif message.content.startswith('!wolframimage'):
       question = message.content[13:]  
       question = reformat_question(question)
       async with aiohttp.ClientSession() as session:
            async with session.get("https://api.wolframalpha.com/v1/simple?appid="+ str(app_id_wolfram) +"&i="+ str(question.replace(" ", "+")) + "%3F") as resp:
                if resp.status != 200:
                    return await message.channel.send('Could not download file...')
                data = io.BytesIO(await resp.read())
                await message.channel.send(file=discord.File(data, 'results.png'))


   elif message.content.startswith('!wolfram'):
       question = message.content[8:]   
       question = reformat_question(question)
       await message.channel.send("Question: " + str(question))
       answer = wolfram_text_answer(question)
       await message.channel.send("Answer: " + str(answer))
       add_to_history(question, answer)
       save_history(history_list)

   elif '!help' in message.content:
       await message.channel.send(helptext)

client.run(keylist[1]) 