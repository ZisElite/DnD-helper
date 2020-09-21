import discord
import asyncio

import dice
import character

races = {1: "Dragonborn",
         2: "Dwarf",
         3: "Elf",
         4: "Gnome",
         5: "Half-Elf",
         6: "Halfing",
         7: "Half-Orc",
         8: "Human",
         9: "Tiefling"}

classes = {1: "Barbarian",
           2: "Bard",
           3: "Cleric",
           4: "Druid",
           5: "Fighter",
           6: "Monk",
           7: "Paladin",
           8: "Ranger",
           9: "Rogue",
           10: "Sorcerer",
           11: "Warlock",
           12: "Wizard"}

skills = {1: "Acrobatics",
          2: "Animal Handling",
          3: "Arcana",
          4: "Athletics",
          5: "Deception",
          6: "History",
          7: "Insight",
          8: "Medicine",
          9: "Nature",
          10: "Perception",
          11: "Performance",
          12: "Persuasion",
          13: "Religion",
          14: "Sleight of Hand",
          15: "Stealth",
          16: "Survival"}

#notes
#-----------------------------------------------------!!!!!!!!!!!!!!!!!!!
async def characterCreation(client, author):
    
    def check(message):
        return message.author == author and message.channel.type == discord.ChannelType.private

    await author.send("Starting new character creation")
    await asyncio.sleep(1)
#setting name--------------------------------------------------------------
    name = ""
    await author.send("What is the character's name?")
    name = await client.wait_for("message", check = check)
    name = name.content
#setting race--------------------------------------------------------------
    race = ""
    await author.send("Select " + name + "'s race (1/2/3..):\n" +
    "\n".join([(str(key) + ". " + value) for key, value in races.items()]))
    while(True):
        race = await client.wait_for("message", check = check)
        try:
            race = int(race.content)
        except:
            await author.send("Please enter a number from 1 to 9")
            print(author.name + " entered non numerical answer for race")
            continue
        else:
            print(author.name + " entered valid answer for race")
        if race > 0 and race < 10:
            break
        await author.send("Please enter a number from 1 to 9")

#setting class-------------------------------------------------------------
    clas = ""
    await author.send("Select "+ name + "'s class (1/2/3...):\n" +
    "\n".join([(str(key) + ". " + value) for key, value in classes.items()]))
    while(True):
        clas = await client.wait_for("message", check = check)
        try:
            clas = int(clas.content)
        except:
            await author.send("Please enter a number from 1 to 12")
            print(author.name + " entered non numerical answer for class")
            continue
        else:
            print(author.name + " entered valid answer for race")
        if clas > 0 and clas < 13:
            break
        await author.send("Please enter a number from 1 to 12")
#setting stats-------------------------------------------------------------
    stats = []
    await author.send("I will now roll for your stats. I will present you with 2 sets of 6 numbers.\n" +
                      "Choose the set you wish to use and assign each value as you see fit\n" +
                      "Enter the stats in the following format:\n" +
                      "strength, dexterity, constitution, intelligence, wisdom, charisma")
    sets = dice.roll_stats()
    sets[0].sort()
    sets[1].sort()
    await author.send("First set: " + str(sets[0]).strip("[]") + "\n" +
                      "Second set: " + str(sets[1]).strip("[]") + "\n")
    while(True):
        stats = await client.wait_for("message", check = check)
        try:
            stats = [int(x) for x in stats.content.strip(" ").split(",")]
        except:
            await author.send("Please answer in the format of str, dex, con, int, wis, cha")
            print(author.name + " entered wrongly formatted input for ability scores")
            continue
        else:
            print(author.name + " entered valid input for ability scores")
        stats.sort()
        if stats in sets:
            break
        await author.send("Please make sure your input is correct")
#setting skill proficiencies-----------------------------------------------
    skill = []
    await author.send("Which skills is "+ name + " proficient at (1, 2, 3,...):\n" +
    "\n".join([(str(key) + ". " + value) for key, value in skills.items()]))
    while(True):
        skill = await client.wait_for("message", check = check)
        try:
            skill = [int(x) for x in skill.content.strip(" ").split(",")]
        except:
            await author.send("Please choose numbers between 1 and 16")
            print(author.name + " entered wrongly formatted input for skills")
            continue
        else:
            print(author.name + " entered valid answer for skills")
        skill.sort()
        if len(skill) > 0 and skill[0] > 0 or skill[len(skill) - 1] < 17:
            break
        await author.send("Please choose numbers between 1 and 16")
#setting level-------------------------------------------------------------
    level = 1
    await author.send("What is " + name + "'s level?")
    while(True):
        ans = await client.wait_for("message", check = check)
        try:
            level = int(ans.content)
        except:
            await author.send("Please enter a number between 1 and 20")
            print(author.name + " entered non numerical answer for level")
            continue
        else:
            print(author.name + " entered valid answer for level")
        if level > 0 or level < 21:
            break
        await author.send("Please enter a number between 1 and 20")
#--------------------------------------------------------------------------
    await author.send("Summoning " + name + " to the material plane")