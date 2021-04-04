import math
import random
import re

#regular expressions used to filter the input
regex_rolls = "^(?:[1-9]{1}[0-9]{1}|[1-9]{1})d(?:2|4|6|8|10|12|20|100){1}$"
regex_custom = "^(?:[1-9]{1}[0-9]{1}|[1-9]{1})d[0-9]+$"
regex_modifiers = "^(?:[+]|[-]){1}(?:[1-9]{1}[0-9]{1}|[1-9]{1})$"
regex_text = "^(?:adv|dis|slashing|sl|piercing|rc|bludgeoning|bg|poison|ps|acid|ac|fire|fr|cold|cl|radiant|rd|necrotic|nc|lightning|lt|thunder|th|force|frc|psychic|psy)$"

texts = ["adv", "dis", "slashing", "sl", "piercing", "rc", "bludgeoning", "bg", "poison", "ps", "acid", "ac", "fire", "fr", 
        "cold", "cl", "radiant", "rd", "necrotic", "nc", "lightning", "lt", "thunder", "th", "force", "frc", "psychic", "psy"]

def analyze_input(ctype, inp):
    if ctype in ["simple", "custom"]:                                                #if roll type is either simple or custm
        roll = inp.split()                                                           #split input
        if len(roll) < 2:                                                            #if input has only 1 element, return error message
            return ("No dice were given")                                             
        elif len(roll) > 2:                                                          #if input has more than 2 elements, return error message
            return("Too many inputs")
        if ctype == "simple":                                                        #if the input is a simple roll
            if re.match(regex_rolls, roll[1]):                                       #if the input matches the acceptable die format
                data = roll_dice([0, 0], [int(x) for x in roll[1].split("d")])       #roll dice and store results in data
                out = output_generator(ctype, data, roll[1])                         #create output and store it in out
                return(out)                                                          #return out to bot to print
            else:                                                                    #else, the input format is wrong, return error message
                return("Wrong format")
        elif ctype == "custom":                                                      #elif the input is a custom roll
            if re.match(regex_custom, roll[1]):                                      #if the input matches the acceptable die format
                data = roll_dice([0, 0], [int(x) for x in roll[1].split("d")])       #roll dice and store results in data
                out = output_generator(ctype, data, roll[1])                         #create output and store it in out
                return(out)                                                          #return out to bot to print
            else:                                                                    #else, the input format is wrong, retur error message
                return("Wrong format")
    else:
        dice = 0
        modifiers = 0
        texts = 0
        data = [[], [], [], [], []]                                                  #data to be given to the output_generator
        rolls = inp.split(",")                                                       #split string at ","
        for i in range(0, len(rolls)):                                               #iterate through all elements of rolls
            roll = rolls[i].split()                                                  #split rolls[i] at all whitespaces, keeping only non-whitespace parts
            if i == 0:                                                               #if this is the first iteration
                roll.pop(0)                                                          #remove the first element, which is the command
            if len(roll) > 3:                                                        #if roll has more than 3 elements, return error message
                return ("Too many elements")
            set_data = [[0,0], 0, ""]                                                #initialize singlular_data list, essentialy reseting the list
            for j in range(0, len(roll)):                                            #iterate through the roll elements
                if re.match(regex_rolls, roll[j]):                                   #if roll[j] matches the acceptable die format
                    if set_data[0] == [0, 0]:                                        #if this is the first die in the roll
                        set_data[0] = [int(x) for x in roll[j].split("d")]           #split roll[j] at d, make the elements int and store them
                    else:                                                            #else, a die format was found earlier in the same roll, return error message
                        return ("More than one die in a set")
                elif re.match(regex_modifiers, roll[j]):                             #elif roll[j] matches the acceptable modifier format
                    if set_data[1] == 0:                                             #if this is the first modifier in roll
                        set_data[1] = int(roll[j])                                   #convert roll[j] to int and store it
                    else:                                                            #else, a modifier format was found earlier in the same roll, return error message
                        return ("More than one modifiers in a set")
                elif re.match(regex_text, roll[j]):                                #elif roll[j] matches the acceptable text format
                    if set_data[2] == "":                                            #if this is the first text in roll
                        set_data[2] = roll[j]                                        #store roll[j]
                    else:                                                            #else, a text format was found earlier in the same roll, return error message
                        return("More than one damage/adv type in a set")
                else:                                                                #else, roll[j] is not of acceptable format, return error message
                    return ("Wrong format")
            check = validate_data(ctype, [dice, modifiers, texts])                   #after every roll, check if the data are fine
            if  check != "ok":                                                       #if the check returns an error, return that error message
                return (check)
            roll_results = roll_dice([""], set_data[0])                            #roll dice and store it in roll_results
            data[0].append(roll_results[0])                                          #append roll total to data totals
            data[1].append(roll_results[1])                                          #append individual rolls to data individual rolls
            data[2].append(set_data[0])                                              #append dice data
            data[3].append(set_data[1])                                              #append modifier to data modifiers
            data[4].append(set_data[2])                                              #append roll text to data texts
        out = output_generator(ctype, data, "")
        return(out)                                                                 #after analysis finish, return the extracted data

def validate_data(ctype, instances):
    check = "ok"
    if ctype == "damage":
        if instances[2] in texts[0:2]:                                               #if adv/dis is in damage roll, return error message
            check = "adv/dis was given instead of damage type"
        elif instances[0] > instances[2]:                                            #if there are more types than rolls, return error message
            check = "Missing damage types"
        elif instances[0] < instances[2]:                                            #if there are more rolls than types, return error message
            check = "Missing dice rolls"
        elif instances[0] < instances[1]:                                            #if there are more modifiers than rolls/types, return error message
            check = "Standalone modifiers were given"
    else:
        if instances[1] > 1 and instances[2] > 1:                                    #if more than one modifier and adv/dis are given, return error message
            check = "Only 1 modifier and adv/dis allowed"
        elif instances[1] > 1:                                                       #if more than one modifier is given, return error message
            check = "Only 1 modifier allowed"
        elif instances[2] > 1:                                                       #if more than one adv/dis is given, return error message
            check = "Only 1 advantage allowed"
    return (check)

def roll_dice(rtype, data):
    rolls = [0, []]
    if rtype[0] == "20":                                                             #if this is a d20 roll
        roll = random.randint(1, 20)
        rolls[0] = roll
        rolls[1].append(roll)
        if rtype[1] == "adv":                                                        #if it is adv, roll 2nd die and choose the higher
            roll2 = random.randint(1, 20)
            rolls[1].append(roll2)
            if roll2 > roll:
                rolls[0] = roll2
        elif rtype[1] == "dis":                                                      #if it is dis, roll 2nd die and choose the lower
            roll2 = random.randint(1, 20)
            rolls[1].append(roll2)
            if roll2 < roll:
                rolls[0] = roll2
        return (rolls)
    else:                                                                            #else, it is a general roll
        for i in range (0, data[0]):                                                 #roll data[0] times, add the result to the list and increase the total
            rolls[1].append(random.randint(1, data[1]))
            rolls[0] += rolls[1][i]
        return (rolls)

def output_generator(ctype, data, inp):
    out = ""
    roll = [0, [0,0]]
    if ctype == "simple" or ctype =="custom":                                        #if is is simple or custom roll return the message
        out += " rolled " + inp  + " for a total of " + str(data[0])
        if len(data[1]) > 1:
            out += " (" + ", ".join([str(x) for x in data[1]]) + ")"
    else:                                                                            #the first part of the message depends on the type of roll
        if ctype == "attack":
            out += " attacks for a total of "
        elif ctype == "damage":
            out += " deals damage for a total of "
        elif ctype == "skill":
            out += " attempts to use a skill for a total of "
        else:
            out += " attempts to save for a total of "
        if ctype == "damage":                                                        #if the roll type is damage, use the following format
            out += str(sum(data[0]) + sum(data[3])) + ": "                           #total dice + total modifiers + ": "
            for i in range(0, len(data[0])):                                         #for each roll, sum the total with modfier + text + " damage"
#                out += str(data[0][i]) + " " + data[4][i] + " damage"
                out += str(data[0][i])
                if data[3][i] > 0:
                    out += " +" + str(data[3][i])
                elif data[3][i] < 0:
                    out += " " + str(data[3][i])
                out += " " + data[4][i] + " damage"
                if len(data[1][i]) > 1:                                              #if more than one die were rolled, show all the results
                    out += " (" + ", ".join([str(x) for x in data[1][i]]) + ")"
                if i != len(data[0]) - 1:                                            #add ", " after each iteration to separate them, unless it is the last one
                    out += ", "
        else:                                                                                                                                                #for attack, skill and save types
            adv = False
            mod = False
            if "adv" in data[4]:                                                                                                                             #if it is advantage
                roll = roll_dice(["20", "adv"], "")                                                                                                          #roll the 2 d20s
                out += str(sum(data[0]) + sum(data[3]) + roll[0]) + ": rolled " + str(roll[0]) + ", adv (" + ",".join([str(x) for x in roll[1]]) + ")"     #total extra dice + modifier + d20 + both d20s
                adv = True
            elif "dis" in data[4]:                                                                                                                           #if it is dis, same as adv
                roll = roll_dice(["20", "dis"], "")                                                                     
                out += str(sum(data[0]) + sum(data[3]) + roll[0]) + ": rolled " + str(roll[0]) + ", dis (" + ",".join([str(x) for x in roll[1]]) + ")"
                adv = True
            else:                                                                                                                                            #else, it has no adv or dis, roll d20, add modifier + extra dice
                roll = roll_dice(["20", ""], "")
                out += str(sum(data[0]) + sum(data[3]) + roll[0]) + ": rolled " + str(roll[0])
            if sum(data[3]) != 0:                                                                                                                            #if there is a modifier, show it
                if adv:
                    out += ", "
                out += str(sum(data[3])) + " modifier"
                mod = True
            for i in range(0, len(data[1])):                                                                                                                 #if there are extra dice, show them one by one
                if sum(data[1][i]) != 0:
                    if adv or mod:
                        out += ", "
                    out += "extra " + str(data[2][i][0]) + "d" + str(data[2][i][1]) + " for " + str(data[0][i])
                    if len(data[1][i]) > 1:                                                                                                                  #if more than one die were rolled, show them all
                        out += " (" + ", ".join([str(x) for x in data[1][i]]) + ")"
    return (out)