import math
import random
import re

types = "(?:\s+(?:slashing|sl|piercing|rc|bludgeoning|bg|poison|ps|acid|ac|fire|fr|cold|cl|radiant|rd|necrotic|nc|lightning|lt|thunder|th|force|frc|psychic|psy))?$"

def roll_selection(ctype, message):
    if ctype == "simple":
        roll = simple_roll(ctype, message)
    elif ctype == "attack":
        roll = attack_roll(ctype, message)
    elif ctype == "damage":
        pass
    elif ctype == "skill":
        pass
    elif ctype == "save":
        pass
    elif ctype == "contesting":
        pass
    elif ctype == "custom":
        pass
    
    return (roll)

#removes the command from the input string, keeping only the rolls and seperating them in a list
def command_strip(ctype, message):
    if ctype == "simple" or ctype == "custom":
        return (message.split()[1:])
    else:
        if message.startswith("!attackroll"):
            return (message[12:].split(","))
        else:
            return (message[5:].split(","))

#searches for specific roll format, depending on the type of roll
def find_rolls(ctype, rolls):
    if ctype == "simple" or ctype == "custom":
        match = re.findall("^(?:[0-9]+d[0-9]+){1}$", rolls)
        return match
    elif ctype == "attack":
        rolls = rolls.lstrip()
        rolls = rolls.rstrip()
        match = re.findall("^(?:[0-9]+d[0-9]+\s+)?(?:(?:[+]|[-])[0-9]+\s+)?(?:(?:adv|dis))?", rolls)
        return match
    #regex = "(?:[0-9]+d[0-9]+)?\s+(?:(?:[+]|[-])[0-9]+)?\s+(?:(?:(?:adv|dis){1}|[0-9]+))?"
    return ("no")

#extracts the roll data
def extract_roll(ctype, matches):
    if ctype == "simple" or ctype == "custom":
        return ([int(x) for x in matches[0].split("d")])
    else:
        data = []
        for match in matches:
            roll = []
            print(matches)
            temp_data = match.split()
            print(temp_data)
            if len(temp_data) == 1:
                if temp_data[0].startswith("+") or temp_data[0].startswith("-"):
                    roll = [[0,0], int(temp_data[0]), ""]
                else:
                    try:
                        roll = [[int(x) for x in temp_data[0].split("d")], 0, ""]
                    except:
                        roll = [[0,0], 0, temp_data[0]]

            if len(temp_data) == 2:
                if temp_data[0].startswith("+") or temp_data[0].startswith("-"):
                    roll = [[0,0], int(temp_data[0]), temp_data[1]]
                elif temp_data[1].startswith("+") or temp_data[1].startswith("-"):
                    roll = [[int(x) for x in temp_data[0].split("d")], int(temp_data[1]), ""]
                else:
                    roll = [[int(x) for x in temp_data[0].split("d")], 0, temp_data[1]]

            elif len(temp_data) == 3:
                roll = [[int(x) for x in temp_data[0].split("d")], int(temp_data[1]), temp_data[2]]
            data.append(roll)
        return (data)

#calculates the dice outcome
def calculate_roll(ctype, data):
    if ctype == "simple" or ctype == "complex":
        if check_die_type(ctype, data[1]):
            rolls = []
            sum = 0
            for i in range(0, data[0]):
                rolls.append(random.randint(1, data[1]))
                sum += rolls[i]
            rolls.insert(0, sum)
            return rolls
        return "error"
    else:
        if check_die_type(ctype, data):
            roll = 0
            advdis = []
            extra = []
            roll1 = random.randint(1, 20)
            if data[0][2] != "":
                roll2 = random.randint(1,20)
                advdis.append(roll1)
                advdis.append(roll2)
                if data[0][2] == "adv":
                    if roll1 >= roll2:
                        roll = roll1
                    else:
                        roll = roll2
                else:
                    if roll1 <= roll2:
                        roll = roll1
                    else:
                        roll = roll2
            else:
                roll = roll1
            roll += data[0][1]
            if data[0][0][0] > 0:
                sum = 0
                for i in range(0, data[0][0][0]):
                    extra.append(random.randint(1, data[0][0][1]))
                    sum += extra[i]
                extra.insert(0, sum)
            return ([roll, data[0][1], advdis, extra])
                

        return "error"

#check if die is of acceptable range
def check_die_type(ctype, data):
    if ctype == "simple":
        if data in [2, 4, 6, 8, 10, 12, 20, 100]:
            return True
        return False
    else:
        for x in data:
            if x[0][1] not in [0, 2, 4, 6, 8, 10, 12, 20, 100]:
                return False
            return True
        

        

#General format for rolls, more specialized rolls are below
def simple_roll(ctype, message):
    roll = command_strip(ctype, message)
    if len(roll) != 1:
        return ("Invalid number of inputs")
    match = find_rolls(ctype, roll[0])
    if len(match) != 1:
        return ("Invalid input format")
    data = extract_roll(ctype, match)
    total = calculate_roll(ctype, data)
    if total == "error":
        return ("Invalid die type")
    if data[0] == 1:
        return (match[0] + " rolled for a total of " + str(total[0]))
    return (match[0] + " rolled for a total of " + str(total[0]) +
            " (" + ", ".join([str(x) for x in total[1:]]) + ")")

#specialized roll for attacks, accepts a chain of attack rolls in the following format: <rolls>d<range> <modifier> <type>, ...
def attack_roll(ctype, message):
    rolls = command_strip(ctype, message)
    if len(rolls) != 1:
        return ("Not enough inputs")
    matches = find_rolls(ctype, rolls[0])
    if len(matches) != 1:
        return ("Invalid input format")
    data = extract_roll(ctype, matches)
    print(data)
    total = calculate_roll(ctype, data)
    if total == "error":
        return ("Invalid dice types")
    reply = "Attacking for " + str(total[0]) + " :"
    if data[0][2] == "adv" or data[0][2] == "dis":
        reply += data[0][2] + "(" + str(total[2][0]) + ", " + str(total[2][1]) + ")"
    if data[0][1] != 0:
        reply += ", modifier of " + str(data[0][1])
    if data[0][0] != [0,0]:
        if data[0][0][0] > 1:
            return (reply + ", extra " + str(data[0][0][0]) + "d" + str(data[0][0][1]) + " for " + str(total[3][0]) + " (" + ", ".join([str(x) for x in total[3][1:]]) + ")")
        return (reply + ", extra " + str(data[0][0][0]) + "d" + str(data[0][0][1]) + " for " + str(total[3][0]))
    return (reply)

def custm_roll(roll):
    modifier = 0
    if len(roll) > 1:
        try:
            modifier += int(roll[1])
        except:
            return("The provided modifier is invalid")


        pass;
    return roll


#Generate random character stats, using the "4d6 drop the lower die" system
def roll_stats():
    sets = []
    for i in range (0,2):
        stats = []
        for j in range(0,6):
            dice = []
            for n in range(0, 4):
                random.seed(random.random()* random.random())
                dice.append(random.randint(1, 6))
            dice.sort()
            dice.pop(0)
            stats.append(sum(dice))
        sets.append(stats)
    return sets
    
