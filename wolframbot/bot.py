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


print(bftranslator("4(1/2"))

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
       if "bf" in question:
           
           bftranslator
       await message.channel.send("Question: " + str(question))
       res = client_wolfram.query(question)
       answer = next(res.results).text
       await message.channel.send("Answer: " + str(answer))


   elif '!help' in message.content:
       await message.channel.send('use format !wolfram {question} in standard wolfram format')

client.run(keylist[1]) 