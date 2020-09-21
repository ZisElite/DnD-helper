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

#make dictionaries for classes, races,skills,stats
#change error message to ligal numbers
#-----------------------------------------------------!!!!!!!!!!!!!!!!!!!
async def characterCreation(client, author):
    
    def check(message):
        return message.author == author and message.channel.type == discord.ChannelType.private

    name = ""
    await author.send("Starting new character creation")
    await asyncio.sleep(1)
    #setting name---------------------------------------------------------
    await author.send("What is the character's name?")
    confirmation = "n"
    while(confirmation == "n"):  
        name = await client.wait_for("message", check = check)
        name = name.content
        if name.strip() == "":
            await author.send("Please enter a valid name")
            continue
        
        await author.send("Are you sure about this name (y/n): " + name)
        while(True):
            confirmation = await client.wait_for("message", check = check)
            confirmation = confirmation.content
            if confirmation in ("y", "n"):
                break
            
            await author.send("Please enter a valid answer")
        if confirmation == "n":
            await author.send("What is the character's name?")
    #setting race----------------------------------------------------------
    race = ""
    await author.send("Select " + name + "'s race (1/2/3..):\n" +
    "\n".join([(str(key) + ". " + value) for key, value in races.items()]))
    confirmation = "n"
    while(confirmation == "n"):
        race = await client.wait_for("message", check = check)
        try:
            race = int(race.content)
        except:
            await author.send("Please enter a number from 1 to 9")
            print(author.name + " entered non numerical answer")
            continue
        else:
            print(author.name + " entered valid answer")
        if race < 0 or race > 9:
            await author.send("Please enter a number from 1 to 9")
            continue
        await author.send("Are you sure about this race (y/n): " + str(race))
        while(True):
            confirmation = await client.wait_for("message", check = check)
            confirmation = confirmation.content
            if confirmation in ("y", "n"):
                break
            
            await author.send("Please enter a valid answer")
        if confirmation == "n":
            await author.send("Select " + name + "'s race (1/2/3..):\n" +
                      "1. Human\n" +
                      "2. Elf\n" +
                      "3. Dwarf")
    #setting class----------------------------------------------------------
    clas = ""
    await author.send("Select "+ name + "'s class (1/2/3...):\n" +
                      "1. Fighter\n" +
                      "2. Ranger\n" +
                      "3. Wizard")
    confirmation = "n"
    while(confirmation == "n"):
        clas = await client.wait_for("message", check = check)
        clas = clas.content
        if int(clas) < 0 or int(clas) > 3:
            await author.send("please choose a valid race")
            continue

        await author.send("Are you sure about this class (y/n): " + clas)
        while(True):
            confirmation = await client.wait_for("message", check = check)
            confirmation = confirmation.content
            if confirmation in ("y", "n"):
                break
            
            await author.send("Please enter a valid answer")
        if confirmation == "n":
            await author.send("Select "+ name + "'s class (1/2/3...):\n" +
                      "1. Fighter\n" +
                      "2. Ranger\n" +
                      "3. Wizard")
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
        stats = [int(x) for x in stats.content.strip(" ").split(",")]
        stats.sort()
        if stats in sets:
            break
        await author.send("Please make sure your input is correct")
    #setting skill proficiencies-----------------------------------------------
    skills = []
    await author.send("Which skills is "+ name + " proficient at (1, 2, 3,...):\n" +
                      "1. Acrobatics\n" +
                      "2. Animal Handling\n" +
                      "3. Arcana")
    confirmation = "n"
    while(confirmation == "n"):
        skills = await client.wait_for("message", check = check)
        skills = [int(x) for x in skills.content.strip(" ").split(",")]
        skills.sort()
        if len(skills) > 0 and skills[0] < 1 or skills[len(skills) - 1] > 3:
            await author.send("please choose numbers between 1 and 3")
            continue

        await author.send("Are you sure about these skills (y/n): " + str(skills))
        while(True):
            confirmation = await client.wait_for("message", check = check)
            confirmation = confirmation.content
            if confirmation in ("y", "n"):
                break
            
            await author.send("Please enter a valid answer")
        if confirmation == "n":
            await author.send("Which skills is "+ name + " proficient at (1, 2, 3,...):\n" +
                      "1. Acrobatics\n" +
                      "2. Animal Handling\n" +
                      "3. Arcana")
    #setting level-------------------------------------------------------------
    level = 1
    await author.send("What is " + name + "'s level?")
    confirmation = "n"
    while(confirmation == "n"):
        ans = await client.wait_for("message", check = check)
        level = int(ans.content)
        if level < 1 or level > 20:
            await author.send("Please enter a number between 1 and 20")
            continue
    await author.send("Are you sure " + name + " is level " + str(level) + "?")
    while(True):
        confirmation = await client.wait_for("message", check = check)
        confirmation = confirmation.content
        if confirmation in ("y", "n"):
            break
    if confirmation == "n":
        await author.send("What is " + name + "'s level?")

            
