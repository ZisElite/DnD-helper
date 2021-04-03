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

inp = input("Enter roll")
ctype = "attack"

if ctype in ["simple", "custom"]:                                                #if roll type is either simple or custm
    roll = inp.split()                                                           #split input
    if len(roll) < 2:                                                            #if input has only 1 element, return error message
        print ("No dice were given")                                             
    elif len(roll) > 2:                                                          #if input has more than 2 elements, return error message
        print("Too many inputs")
        if ctype == "simple":                                                    #if the input is a simple roll
            if re.match(regex_rolls, inp):                                       #if the input matches the acceptable die format
                print([int(x) for x in inp.split("d")])                          #split input at d, make the elements int and return them
            else:                                                                #else, the input format is wrong, return error message
                print("Wrong format")
        elif ctype == "custom":                                                  #elif the input is a custom roll
            if re.match(regex_custom, inp):                                      #if the input matches the acceptable die format
                print ([int(x) for x in inp.split("d")])                         #split input at d, make the elements int and return them
            else:                                                                #else, the input format is wrong, retur error message
                print("Wrong format")
else:
    dice = 0
    modifiers = 0
    texts = 0
    data = []                                                                    #data to be given to calculator
    rolls = inp.split(",")                                                       #split string at ","
    for i in range(0, len(rolls)):                                               #iterate through all elements of rolls
        roll = rolls[i].split()                                                  #split rolls[i] at all whitespaces, keeping only non-whitespace parts
        if i == 0:                                                               #if this is the first iteration
            roll.pop(0)                                                          #remove the first element, which is the command
        if len(roll) > 3:                                                        #if roll has more than 3 elements, return error message
            print ("Too many elements")
        singular_data = [[0,0], 0, ""]                                           #initialize singlular_data list, essentialy reseting the list
        for j in range(0, len(roll)):                                            #iterate through the roll elements
            if re.match(regex_rolls, roll[j]):                                   #if roll[j] matches the acceptable die format
                if singular_data[0] == [0, 0]:                                   #if this is the first die in the roll
                    singular_data[0] = [int(x) for x in roll[j].split("d")]      #split roll[j] at d, make the elements int and store them
                else:                                                            #else, a die format was found earlier in the same roll, return error message
                    print ("More than one die in a set")
            elif re.match(regex_modifiers, roll[j]):                             #elif roll[j] matches the acceptable modifier format
                if singular_data[1] == 0:                                        #if this is the first modifier in roll
                    singular_data[1] = int(roll[j])                              #convert roll[j] to int and store it
                else:                                                            #else, a modifier format was found earlier in the same roll, return error message
                    print ("More than one modifiers in a set")
            elif re.match(regex_text, roll[j]):                                  #elif roll[j] matches the acceptable text format
                if singular_data[2] != "":                                       #if this is the first text in roll
                    singular_data[2] = roll[j]                                   #store roll[j]
                else:                                                            #else, a text format was found earlier in the same roll, return error message
                    print("More than one damage/adv type in a set")
            else:                                                                #else, roll[j] is not of acceptable format, return error message
                print ("Wrong format")
        check = validate_data(ctype, [dice, modifiers, texts])                   #after every roll, check if the data are fine
        if  check != "ok":                                                       #if the check returns an error, return that error message
            print (check)
        data.append(singular_data)                                               #after every iteration of roll[i], append singular_data to data
    print(data)                                                                  #after analysis finish, return the extracted data

def validate_data(ctype, instances):
    check = "ok"
    if ctype == "attack":
        if instances[1] > 1 and instances[2] > 1:
            check = "Only 1 modifier and adv/dis allowed"
        elif instances[1] > 1:
            check = "Only 1 modifier allowed"
        elif instances[2] > 1:
            check = "Only 1 advantage allowed"
    elif ctype == "damage":
        if instances[2] in texts[0:2]:
            check = "adv/dis was given instead of damage type"
        elif instances[0] > instances[2]:
            check = "Missing damage types"
        elif instances[0] < instances[2]:
            check = "Missing dice rolls"
        elif instances[0] < instances[1]:
            check = "Empty modifiers were inputed"
    return (check)

def calculate(data):
    pass