class Character:
    def _init_(self, name, race, clas, stats, skills, level):
        self.name = name
        self.race = race
        self.clas = clas
        self.stats = stats
        self.skills = skills
        self.level = level

    def calculate_saving_throw(self):
        pass

    def calculate_stats(self):
        pass

    def calculate_skills(self):
        pass

    def calculate_armor_health_speed(self):
        pass
