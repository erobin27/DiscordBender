import discord
import os
import asyncio
import emoji
import random
import time
#13 spaces = 1 emoji
client = discord.Client()

key = '!'
checkMark = ':white_heavy_check_mark:'



def isCustomEmoji(emoji):
  pass

async def fillPlayers(reactionList):
  players = []
  playerDict = {}
  reactionList.pop() #removes the checkmark emoji from list
  for elem in reactionList:
    players.append(elem.emoji)
    users = await elem.users().flatten()
    playerDict[elem.emoji] = users[0]

  return [players,playerDict]




'''REACTION EMOJI LOGIC'''
def check(reaction, user):
  try:
    return emoji.demojize(reaction.emoji) == checkMark
  except:
    return reaction.emoji.name == checkMark

def messageReactionList(message):
  return message.reactions

async def userReactionResponse():
  try:
    reaction, user = await client.wait_for('reaction_add',
    timeout = 90.0,
    check=check)

  except asyncio.TimeoutError:
    return False
  else:
    return True

async def clearAllReactions(message):
  reactions = messageReactionList(message)
  for r in reactions:
    await message.clear_reaction(r)




'''SHOT ROULETTE GAME'''
async def printWinner(winner, channel):
  msg = '🎉' + winner.mention + ' drink up!'
  return await channel.send(msg)

async def editPlayersMessage(players, message):
  msg = ''
  for i in players:
    try:
      msg += str(i)
    except:
      msg += str(emoji.demojize(i))
  await message.edit(content=msg)

async def printPlayersInit(players, channel):
  msg = ''
  for i in players:
    try:
      msg += str(i)
    except:
      msg += str(emoji.demojize(i))
  
  return await channel.send(msg)

def moveListElements(playerList):
  var = playerList.pop()
  playerList.insert(0,var)
  return playerList
def fillPlayerDictionary(players):
  playerDict = {}
  for p in players:
    playerDict[p] = p
  
  return playerDict

def findWinner(players, loserKey):
  for p in players:
    if p != loserKey:
      return p

async def spinEmojis(message, players, times):
  while times > 0:
    time.sleep(.8)
    players = moveListElements(players)
    await editPlayersMessage(players, message)
    times -= 1

async def eliminateEmojis(message, players):
  playerCount = len(players)
  rList = random.sample(range(playerCount),playerCount-1)
  #playerDict = fillPlayerDictionary(players)
  time.sleep(4.0)
  index=0
  while index < playerCount-1:
    players[rList[index]] = '❌'
    #'             '
    await editPlayersMessage(players, message)
    index += 1
    time.sleep(1.0)
  
  return findWinner(players,'❌')

    







'''SHOT ROULETTE MAIN FUNCTION'''
async def shotRoulette(message):
  reply = await message.channel.send('Select your players by reacting with emojis.\n\nWhen done react with :white_check_mark:')
  
  response = await userReactionResponse()
  
  if not response:
    return False
  
  rMsg = await message.channel.fetch_message(reply.id)
  reactionList = messageReactionList(rMsg)

  temp = await fillPlayers(reactionList)
  players = temp[0] #list of players (emojis)
  playerDict = temp[1] #dictionary dict[emoji] = user
  
  await clearAllReactions(rMsg)
  playerMsg = await printPlayersInit(players, message.channel)
  
  #await spinEmojis(playerMsg,players,rInt)
  winner = await eliminateEmojis(playerMsg, players)
  if winner is None:
    print('ERROR: winner is None')

  await printWinner(playerDict[winner], message.channel)
  #Elim emojis
  #print all emojis
  #randomly replace an emoji with 13 spaces
  #stop once only one emoji is left







'''MESSAGE PARSING LOGIC'''
async def settings():
  pass

async def play(message):
  query = message.content.split()[1].lower();
  if query=='shotroulette':
    await shotRoulette(message)

async def findResponse(message):
  query = message.content.split()[0]
  query = query[1:].lower()
  

  if query == 'settings':
    print('settings')
  if query == 'play':
    await play(message)








'''BOT JOIN LOGIC'''
@client.event
async def on_ready():
  print('Logged in as: {0.user}'.format(client))

@client.event
async def on_message(message):
  if message.author == client.user:
    return
  if message.content.startswith(key):
    await findResponse(message)

@client.event
async def on_reaction_added(reaction, user):
  message = reaction.message
  

client.run(os.getenv('TOKEN'));