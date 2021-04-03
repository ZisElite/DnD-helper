class_saves = ((1, 0, 1, 0, 0, 0), (0, 1, 0, 0, 0, 1), (0, 0, 0, 0, 1, 1),
                (0, 0, 0, 1, 1, 0), (1, 0, 1, 0, 0, 0), (1, 1, 0, 0, 0, 0),
                (0, 0, 0, 0, 1, 1), (1, 1, 0, 0, 0 ,0), (0, 1, 0, 1, 0, 0),
                (0, 0, 1, 0, 0, 1), (0, 0, 0, 0, 1, 1), (0, 0, 0, 1, 1, 0))

race_stats = ((2, 0, 0, 0, 0, 1), (0, 0, 2, 0, 0, 0), (0, 2, 0, 0, 0, 0),
                (0, 0, 0, 2, 0, 0), (0, 0, 0, 0, 0, 2), (0, 2, 0, 0, 0, 0),
                (2, 0, 1, 0, 0, 0), (1, 1, 1, 1, 1, 1), (0, 0, 0, 1, 0, 2))

hit_dice = (12, 8, 8, 8, 10, 8, 10, 10, 8, 6, 8, 6)

movement = ()

class Character:
    def _init_(self, name, race, clas, stats, skills, level):
        self.name = name
        self.race_id = race[0]
        self.race_name = race[1]
        self.class_id = clas[0]
        self.class_name = clas[1]
        self.stats = stats
        self.level = level
        self.saving_throws = class_saves[class_id - 1]

        for x in range(0, 6):
            self.stats[x] += race_stats[x]
        
        self.ability_modifiers = [0, 0, 0, 0, 0, 0]
        for x in range(0, 6):
            self.ability_modifiers[x] = (stats[x] - 10) // 2

        self.skills_proficiencies = []
        for x in range(0, 13):
            if(x + 1 in skills):
                self.skills_proficiencies.append(1)
            else:
                self.skills_proficiencies.append(0)
        
        self.hit_die = hit_dice[self.class_id]
        self.health = (self.hit_die / 2 + 1 + self.ability_modifiers[2]) * level - self.hit_die / 2 - 1
        self.movement = movement[self.race_id - 1]
        self.proficiency = (level - 1) // 4 + 2

    
    def load_character(self):
        pass

    def save_character(self):
        pass
    
    


    