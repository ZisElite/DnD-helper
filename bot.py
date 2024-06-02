import discord
import pickle

#custom
import dice
import character_creation
import helper

makingCharacter = []

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.channel.type != discord.ChannelType.private and message.channel.name == "bot-channel":

        if  message.content.startswith("!hello"):
            await message.channel.send("Hello!")
        
        if message.content.startswith("!helper"):
            reply = helper.reply(str(message.content))
            await message.channel.send(reply)
        
        if message.content.startswith("!roll ") or message.content.startswith("!r "):
            roll = dice.analyze_input("simple", str(message.content))
            await message.channel.send(message.author.display_name + " " + roll)

        if message.content.startswith("!attackroll ") or message.content.startswith("!atr "):
            roll = dice.analyze_input("attack", str(message.content))
            await message.channel.send(message.author.display_name + " " + roll)

        if message.content.startswith("!damagemroll ") or message.content.startswith("!dar "):
            roll = dice.analyze_input("damage", str(message.content))
            await message.channel.send(message.author.display_name + " " + roll)
        
        if message.content.startswith("!skillroll ") or message.content.startswith("!skr "):
            roll = dice.analyze_input("skill", str(message.content))
            await message.channel.send(message.author.display_name + " " + roll)
        
        if message.content.startswith("!saveroll ") or message.content.startswith("!sar "):
            roll = dice.analyze_input("save", str(message.content))
            await message.channel.send(message.author.display_name + " " + roll)

#        if message.content.startswith("!contestingroll ") or message.content.startswith("!cor "):
#            roll = dice.analyze_input("contesting", str(message.content))
#            await message.channel.send(roll)

        if message.content.startswith("!customroll ") or message.content.startswith("!cur "):
            roll = dice.analyze_input("custom", str(message.content))
            await message.channel.send(message.author.display_name + roll)

        if message.content.startswith("!types"):
            await message.channel.send(helper.types())

#       if message.content.startswith("!makechar"):
#           if message.author not in makingCharacter:
#              makingCharacter.append(message.author)
#                await character_creation.characterCreation(client, message.author)
#                makingCharacter.remove(message.author)

    #if message.content.startswith("!test"):

client.run(
# bot key goes here
)
    
