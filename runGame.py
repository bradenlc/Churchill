import discord
import asyncio
import random
import logging
import gameClass

async def threeFailures(game):
  print("Debug")
  #TODO

async def main(game):
  game.gameStarted = True
  
  numOfPlayers = len(game.innedPlayerlist)
  if numOfPlayers > 8:
    game.addRoles(3)
  elif numOfPlayers > 6:
    game.addRoles(2)
  else:
    game.addRoles(1)
  
  await game.sendRolePMs()
  
  game.presidentCounter = random.randrange(0,game.numOfPlayers)
  
  while not game.over:
    await game.genPolicies()
    print("genPolicy complete")
    playerElected = False
    failedElections = 0
    while not playerElected:
      await game.assignPres()
      print("assignPres complete")
      await game.nomination()
      print("nomination complete")
      playerElected = await game.vote()
      print("vote complete")
      if not playerElected:
        if failedElections == 2:
          await threeFailures(game)
        else:
          failedElections += 1
          game.presidentCounter += 1
    game.chancellor = game.nominatedPlayer
    game.nominatedPlayer = False
    await game.checkIfWon()
    print("checkIfWon complete")
    if not game.over:
      await game.client.send_message(game.gameChannel, ("The vote succeeded! President {} and Chancellor {} "
                                                        "are now choosing policies.").format(game.president.name, game.chancellor.name))
      game.lastChancellor = game.president
      game.lastPresident = game.chancellor
      await game.presPolicies()
      print("presPolicies complete")
      enactedPolicy = await game.chancellorPolicies()
      print("chancellorPolicies complete")
      await game.addPolicy(enactedPolicy)
      print("addPolicy complete")
      game.presidentCounter += 1
      await game.checkIfWon()
