import discord
import os
import wolframalpha

keys = open('../keys.txt', 'r').read()
keylist = keys.split(",")

client = discord.Client()
app_idwolfram = keylist[0]
clientwolfram = wolframalpha.Client(app_idwolfram)
 
@client.event
async def on_ready():
   print('We have logged in as {0.user}'.format(client))
 
@client.event
async def on_message(message):
   if message.author == client.user:
       return
 
   if message.content.startswith('!wolfram'):
       question = message.content[8:]   
       await message.channel.send("Question: " + str(question))
       res = clientwolfram.query(question)
       answer = next(res.results).text
       await message.channel.send("Answer: " + str(answer))

   elif '!help' in message.content:
       await message.channel.send('use format !wolfram {question} in standard wolfram format')

client.run(keylist[1])