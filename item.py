import abc
import csv
import random
import typing
from typing import List


class Item(abc.ABC):
    CONDITIONS: List[List[typing.Union[str, float]]] = []
    ITEMS: List[List[str]] = []

    # ss = typing.Union[str,float]


    @classmethod
    def load_conditions(cls) -> None:
        with open('item_attributes', 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                cls.CONDITIONS.append(row)



    @classmethod
    def load_items(cls) -> None:
        with open('item_types', 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                cls.ITEMS.append(row)

    @property
    def name(self):
        return self.__name

    @property
    def condition(self):
        return self.__condition

    @property
    def description(self):
        # return f'{self.condition[0]} {self.name}: {float(self.condition[1])} modifier'
        # return f'{self.condition} {self.name}'
        return f'{self.name}'


    def __init__(self, attributes) -> None:
        self.attributes = attributes
        self.__name = attributes[1]
        Item.load_conditions()
        Item.load_items()
        # cond = Item.CONDITIONS
        # print(f'{self.CONDITIONS}')
        self.__condition = random.choice(self.CONDITIONS)

    def __str__(self):
        return f'{self.__name} {self.__condition}'


class Armor(Item):
    @property
    def added_defense(self):
        return self.__added_defense

    @added_defense.setter
    def added_defense(self, added_defense):
        self.__added_defense = added_defense

    def __init__(self, attributes):
        super().__init__(attributes)

        if float(self.condition[1]) < 1:
            self.__added_defense = (int(float(attributes[3]) * (float(self.condition[1])))) * -1
        else:
            self.__added_defense = int(float(attributes[3]) * (float(self.condition[1])))

    @property
    def itemdesc(self):
        allattrib = ''
        for x in range(len(self.attributes)):

            if x == 0:
                allattrib += f'(Type: {self.attributes[x]} '
            if x == 1:
                allattrib += f'Name: {self.attributes[x]} '
            if x == 2:
                allattrib += f'Attack: {self.attributes[x]} '
            if x == 3:
                allattrib += f'Defense: {self.attributes[x]} '
            if x == 4:
                allattrib += f'Weight: {self.attributes[x]}) '

        return allattrib

class Weapon(Item):
    @property
    def added_attack(self):
        return self.__added_attack

    @added_attack.setter
    def added_attack(self, added_attack):
        self.__added_attack = added_attack

    def __init__(self, attributes):
        super().__init__(attributes)
        # print(attributes[2])
        # print(self.condition)
        if float(self.condition[1]) < 1:
            self.__added_attack = (int(float(attributes[2]) * (float(self.condition[1])))) * -1
        else:
            self.__added_attack = int(float(attributes[2]) * (float(self.condition[1])))

    @property
    def itemdesc(self):
        allattrib = ''
        for x in range(len(self.attributes)):

            if x == 0:
                allattrib += f'(Type: {self.attributes[x]} '
            if x == 1:
                allattrib += f'Name/condition: {self.attributes[x]} {self.condition[1]}'
            if x == 2:
                allattrib += f'Attack: {self.attributes[x]} '
            if x == 3:
                allattrib += f'Defense: {self.attributes[x]} '
            if x == 4:
                allattrib += f'Weight: {self.attributes[x]}) '

        return allattrib

        # self.__added_attack = int(attributes[2] * float(self.condition[1]))

# Item.load_items()
#
# randitem = random.choice(Item.ITEMS)
# print(randitem)
#
# IwitAts = Item(randitem)
# print(IwitAts.description)

#
# sws = Item.load_conditions()
