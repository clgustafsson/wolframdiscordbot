import discord
import os
import wolframalpha
import io
import aiohttp

def bftranslator(bf):
    list = bf.split("(")
    list2 = list[1].split("/")
    fn = int(list[0])*int(list2[1])
    rft = fn+ int(list2[0])
    rfn = list2[1]
    rf = "("+str(rft)+"/"+str(rfn)+")"
    return rf


def findendpindex(start, string):
    counter = 1
    for endi in range(start, len(string)):
        if (string[endi] == '('):
            counter += 1
        if (string[endi] == ')'):
            counter -= 1
            if counter == 0:
                return endi
    return -1

def bf(question):
    while "bf" in question:
        start = question.index("bf")
        replacestring = (bftranslator(question[start +2:findendpindex(start + 4, question)]))
        sub1 = question[:start]
        sub2 = question[findendpindex(start + 4, question)+1:]
        question = sub1 + replacestring + sub2
    return question



keys = open('keys.txt', 'r').read()
keylist = keys.split(",")

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
       question = bf(question)
       await message.channel.send("Question: " + str(question))
       res = client_wolfram.query(question)
       answer = next(res.results).text
       await message.channel.send("Answer: " + str(answer))
   elif message.content.startswith('!imagewolfram'):
       question = message.content[13:]  
       question = bf(question)
       async with aiohttp.ClientSession() as session:
            async with session.get("https://api.wolframalpha.com/v1/simple?appid="+ str(app_id_wolfram) +"&i="+ str(question.replace(" ", "+")) + "%3F") as resp:
                if resp.status != 200:
                    return await message.channel.send('Could not download file...')
                data = io.BytesIO(await resp.read())
                await message.channel.send(file=discord.File(data, 'results.png'))


   elif '!help' in message.content:
       await message.channel.send('use format !wolfram {question} in standard wolfram format to get text answer \nuse format !imagewolfram {question} in standard wolfram format to get full image answer\nuse format bf{num}({num}/{num}) to use mixed form')

client.run(keylist[1]) 