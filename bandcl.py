#!usr/bin/python3
# -*- coding: utf-8 -*-
""" extract data from csv"""


class Band:
    def __init__(self, name=None):
        self.name = name
        self.total_cost = 0
        self.personalities_cost = 0
        self.model_list = []

    def __repr__(self):
        model_str = "Total: {}pts\t(Personalities: {}pts)\n\n".format(self.total_cost, self.personalities_cost)
        for model in self.model_list:
            model_str += str(model) + "\n\n"
        if self.name is not None:
            return "BAND: {}\n{}".format(self.name, model_str)
        else:
            return model_str

    def add_model(self, model):
        self.model_list.append(model)
        self.total_cost += model.cost
        if model.personality is True:
            self.personalities_cost += model.cost

    def remove_model(self, model):
        self.model_list.remove(model)
        self.total_cost -= model.cost
        if model.personality is True:
            self.personalities_cost -= model.cost

    def update_cost(self):
        self.total_cost = 0
        self.personalities_cost = 0
        for model in self.model_list:
            self.total_cost += model.cost
            if model.personality is True:
                self.personalities_cost += model.cost

    def copy_band(self, band):
        self.name = band.name
        for model in self.model_list:
            self.remove_model(model)
        for model in band.model_list:
            new_model = Model()
            new_model.copy_model(model)
            self.add_model(new_model)


class Model:
    def __init__(self, name="My Model"):
        self.name = name
        self.personality = False
        self.cost = 30
        self.combat = 3
        self.quality = 3
        self.capacities_list = []
        self.picture = None

    def __repr__(self):
        if self.personality is True:
            core_str = "{} (Personality): {}pts\nQuality: {}\tCombat: {}\n". \
                format(self.name.encode('utf-8'), self.cost, self.quality, self.combat)
        else:
            core_str = "{}: {}pts\nQuality: {}\tCombat: {}\n". \
                format(self.name.encode('utf-8'), self.cost, self.quality, self.combat)
        if self.capacities_list:
            opt_str = "Capacities: " + self.capacities_list[0].name
            for capacity in self.capacities_list[1:]:
                opt_str += ", " + capacity.name
            core_str += opt_str
        return core_str

    def display(self):
        if self.personality is True:
            core_str = "{} (P) - Q{}+/C{} - {}pts". \
                format(self.name.encode('utf-8'), self.quality, self.combat, self.cost)
        else:
            core_str = "{} - Q{}+/C{} - {}pts". \
                format(self.name.encode('utf-8'), self.quality, self.combat, self.cost)
        return core_str

    def update_cost(self):
        self.cost = 0
        cap_cost = int(int(self.combat) * 5)
        for capacity in self.capacities_list:
            cap_cost += int(capacity.cost)
        self.cost = int(cap_cost * (7 - int(self.quality)) / 2)

    def update_pers(self):
        self.personality = False
        for capacity in self.capacities_list:
            if capacity.personality is True:
                self.personality = True
                break

    def set_quality(self, quality):
        self.quality = int(quality)
        self.update_cost()

    def set_combat(self, combat):
        self.combat = combat
        self.update_cost()

    def set_name(self, name):
        self.quality = name

    def add_capacity(self, capacity):
        capa_already_possessed = False
        for capa in self.capacities_list:
            if capa.name == capacity.name:
                capa_already_possessed = True
        if capa_already_possessed is False:
            self.capacities_list.append(capacity)
        self.update_cost()
        self.update_pers()

    def remove_capacity(self, capacity):
        self.capacities_list.remove(capacity)
        self.update_cost()
        self.update_pers()

    def clean_capacity(self):
        self.capacities_list = []
        self.personality = False
        self.update_cost()

    def copy_model(self, model_src):
        self.name = model_src.name
        self.combat = model_src.combat
        self.quality = model_src.quality
        self.capacities_list = []
        for capa in model_src.capacities_list:
            self.capacities_list.append(capa)
        self.personality = model_src.personality
        self.cost = model_src.cost

    def change_picture(self, pic):
        self.picture = pic


class Capacity:
    def __init__(self, name, cost, personality, help_txt="", text=""):
        self.name = name
        self.help = help_txt
        self.cost = cost
        self.text = text
        self.personality = personality


def load_capacities_from_file(file):
    from io import open
    capacities_list = []
    with open(file, encoding="utf8") as f:
        for line in f:
            file_list = line.split(";")
            if file_list[2] == "X":
                perso = True
            else:
                perso = False
            capacities_list.append(Capacity(file_list[0], int(file_list[1]), personality=perso,
                                            help_txt=file_list[3], text=file_list[4]))
    return capacities_list
