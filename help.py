
def reply(message):
    content = message.split(" ")
    #if it is only the help command, dispay a list of all commands
    if len(content) == 1:
        return ("!helper to display this message\n" +
                "!helper <command> to display how the specified command works" +
                "!type to display all damage types\n" +
                "!roll or !r to make a simple roll\n" +
                "!attackroll or !atr to make an attack\n" +
                "!damageroll or !dar to roll damage\n" +
                "!skillroll or !skr to make a skill check\n" +
                "!saveroll or !sar to make a saving through\n" +
#                "!contestingroll or !cor to make a contesting roll\n" +
                "!customroll or !cur to make a custom roll")

    #if it is !helper + <command>, display how that <command> works
    elif len(content) == 2:
        #show how !roll works
        if content[1] == "!roll" or content[1] == "!r":
            return ("A roll that uses a single type of die without modifiers, f.e. 2d8, 4d4, 1d20, etc.")
        #show how !attackroll, !skillroll and !saveroll works
        elif content[1] == "!attackroll" or content[1] == "!atr" \
            or content[1] == "!skillroll" or content[1] == "!skr" \
            or content[1] == "!saveroll" or content[1] == "!sar":
            return ("A more advanced roll type, you can enter any extra dice that would influence the outcome(like bardic inspiration)," +
                    " your modifier and wehter or not you have advantage or disadvantage.\n" +
                    "  F.e. 1d6 +4 adv, -2 dis, etc.")
        #show how !damageroll works
        elif content[1] == "!damageroll" or content[1] == "!dar":
            return ("An advanced roll type, you can chain all your dice rolls in the following format:\n" +
                    "<amount>d<type> <modifier> <damage type>, ...\n" +
                    "f.e. 2d6 +4 fire, 4d6 -2 bg (to learn more about damage types enter !dmtypes).")

        #show how !contestingroll works ---------POSSIMPLE IMPLEMENTATION IN THE FUTURE
#        elif content[1] == "!contestingroll" or content[1] == "!cor":
#            return ("A contesting roll uses the contestants' modifiers, wether someone has advantage or disadvantage" +
#                    " and any extra dice that might be used, like bardic inspiration.\n" +
#                    "F.e. +3 adv, 1d4 + 5 (this counts as one roll).")

        #show how !customroll works
        elif content[1] == "!customroll" or content[1] == "!cur":
            return ("This is a freely customizable roll, where there range is outside of the" +
                    " regular 7 types, f.e. 3d110, 40d3, 20d21, etc.")
        #show how !type works
        elif content[1] == "!types":
            return ("This command shows you all the damage types.")
        #show how !makechar works
        elif content[1] == "!makechar":
            return ("a guided tutorial to make a playable character, it takes place in a dm with the bot.")
        
        else:
            return("Invalid command")
    else:
        return("Invalid command")

def types():
    return ("the damage types and their shorthand versions are:\n" +
                    "slashing or sl\n" +
                    "piercing or pr\n" +
                    "bludgeoning or bg\n" +
                    "poison or ps\n" +
                    "acid or ac\n" +
                    "fire or fr\n" +
                    "cold or cl\n" +
                    "radiant or rd\n" +
                    "necrotic or nc\n" +
                    "lightning or lt\n" +
                    "thunder or th\n" +
                    "force or frc\n" +
                    "psychic or psy")