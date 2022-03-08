import discord
import os
import wolframalpha
import io
import aiohttp

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

def wolfram_text_answer(question):
    res = client_wolfram.query(question)
    return next(res.results).text


keys = open('keys.txt', 'r').read()
keylist = keys.split(",")

helptext = "use format !wolfram <question> in standard wolfram format to get text answer \nuse format !imagewolfram <question> in standard wolfram format to get full image answer\nuse format bf<num>(<num>/<num>) to use mixed form"

client = discord.Client()
app_id_wolfram = keylist[0]
client_wolfram = wolframalpha.Client(app_id_wolfram)
 
@client.event
async def on_ready():
   print('We have logged in as {0.user}'.format(client))
 
@client.event
async def on_message(message):
   if message.author == client.user:
       return
 
   if message.content.startswith('!wolfram'):
       question = message.content[8:]   
       question = reformat_question(question)
       await message.channel.send("Question: " + str(question))
       answer = wolfram_text_answer(question)
       await message.channel.send("Answer: " + str(answer))
   elif message.content.startswith('!imagewolfram'):
       question = message.content[13:]  
       question = reformat_question(question)
       async with aiohttp.ClientSession() as session:
            async with session.get("https://api.wolframalpha.com/v1/simple?appid="+ str(app_id_wolfram) +"&i="+ str(question.replace(" ", "+")) + "%3F") as resp:
                if resp.status != 200:
                    return await message.channel.send('Could not download file...')
                data = io.BytesIO(await resp.read())
                await message.channel.send(file=discord.File(data, 'results.png'))


   elif '!help' in message.content:
       await message.channel.send(helptext)

client.run(keylist[1]) 