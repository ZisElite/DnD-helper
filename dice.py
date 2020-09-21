import math
import random

def roll(dice):
    nums = dice.strip(" ").split("d")
    try:
        iterations = int(nums[0])
        rang = int(nums[1])
    except:
        return("invalid input")
    if rang not in [2, 4, 6, 8, 10, 12, 20, 100]:
        return ("invalid dice")
    
    rolls = []
    damage = 0
    for i in range (0, iterations):
        random.seed(random.random() * random.random())
        die = random.randint(1, rang)
        damage += die
        rolls.append(str(die))
    return (dice + " rolled for a total of " + str(damage) +
            " damage (" + ", ".join(rolls) + ")")


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
    
