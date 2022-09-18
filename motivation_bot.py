
import discord
import os 
import requests
import json
import random
from replit import db
from keep_alive import keep_alive
from discord.ext import commands

sad_words=[ "sad","depression","angry","tortured"]
words = ["cheers up!","dont worry bro" ,"try hard"]

def update_data(message):
  if "me" in db.keys():
    me = db["me"]
    me.append(message)
    db["me"] = me
  else:
    db["me"] =[message]
  
def delete(index):
  me = db["me"]
  if len(me) > index:
    del me[index]
    db["me"] = me


def get_reply():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " -" + json_data[0]['a']
  return quote

def get_reply1():
  response = requests.get("https://api.chucknorris.io/jokes/random")
  json_data = json.loads(response.text)
  jokes = json_data["value"]
  return jokes

client= commands.Bot(command_prefix='$')

  

@client.event
async def on_ready():
  print('Logged in successful as {0.user}'.format(client))

@client.command()
async def join(ctx):
    channel = ctx.author.voice.channel
    await channel.connect()
@client.command()
async def leave(ctx):
    await ctx.voice_client.disconnect()

@client.event
async def on_message(message):
  if message.author == client.user   :
    return
  option = words
  if "me" in db.keys():
   option = option + db["me"]

  msg =message.content

  
  if msg.startswith('$lodu'):
    await message.channel.send(get_reply())

  if msg.startswith('$munna'):
    await message.channel.send(get_reply1())  

  if any(word in msg for word in sad_words):
    await message.channel.send(random.choice(option))
    print(option)

  if msg.startswith("$new"):
    me = msg.split("$new ",1)[1]
    update_data(me)
    await message.channel.send("updated new message in database")

  if msg.startswith("$del"):
    me =[]
    if "me" in db.keys():
      index =int( msg.split("$del ",1)[1])
      delete(index)
      me = db["me"]
      await message.channel.send(me) 

keep_alive()
client.run(os.getenv('MC'))
################################################################


