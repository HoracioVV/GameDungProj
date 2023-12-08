import random
from typing import Optional, List
from character import Monster
from item import Item


class Dungeon:
    @property
    def name(self):
        return self.__name

    # @name.setter
    # def name(self, name):
    #     self.__name = name

    @property
    def monsters(self):
        return self.__monsters

    @property
    def items(self):
        return self.__items

    @property
    def prior(self):
        return self.__prior

    @prior.setter
    def prior(self, prior):
        self.__prior = prior

    @property
    def next(self):
        return self.__next

    @next.setter
    def next(self, next):
        self.__next = next

    def __init__(self, name, description) -> None:
        self.__name = name
        self.__description = description
        self.__monsters = []
        self.__items = []
        # self.showiteminfo = ''
        # if len(self.__items) > 0:
        #     for i in self.__items:
        #         self.showiteminfo += f'{i.description}, '
        # self.item_type = ''
        # self.item_name = ''
        # self.item_addedattack = ''
        # self.item_addeddefense = ''
        # self.Wgt = ''
        # if len(self.__items) > 0:
        #     for i in self.__items:
        self.__prior = None
        self.__next = None
        self.__monster_list = []
        with open('./monster_names') as f:
            self.__monster_list = f.readlines()

    def generate(self) -> None:
        n = random.randint(0, 4)
        names = random.sample(self.__monster_list, k=n)

        for m in names:
            self.__monsters.append(Monster(m))


    def monster_in_dungeon(self, name): # -> Optional[Monster]
        curmonster = None
        pickedname = f'{name}\n'

        # for monstas in self.__monsters:
        #     print(monstas.name)
        #     # if monstas(name) == True:
        #     #     curmonster = monstas


        # return curmonster


        for monstas in self.__monsters:
            if monstas.name == pickedname or monstas == name:
                curmonster = monstas
                # return monstas
                # return True
            # else:
            #     return None

        return curmonster

        # if name in self.__monsters:
        #     return name
        # else:
        #     return None

    # def Optional[Monster]:
    #     pass

    def __str__(self):
        id = ''
        for x in self.__items:
            id += x.itemdesc
        # if len(self.__items) > 0:
        #     self.showiteminfo = ''
        #     for i in self.__items:
        #         self.showiteminfo += f'{i.description}'

        return f'{self.__name}, {self.__description}, # of monsters in dungeon: {len(self.__monsters)},' \
               f'\nitems in room: {id}'

    def __show_monsters__(self):
        sem = f''

        if len(self.__monsters) == 0:
            return "No monsters (whew!)."
        else:
            for m in self.__monsters:
                # sem = sem
                sem += m.__str__() + '\n'
            return sem


Dun = Dungeon("dung", "Come into my sexy dungeon")
Dun.generate()
# print(Dun.monster_in_dungeon('Cinderbrute'))
# print(Dun.monsters)
print(Dun.monster_in_dungeon('Nightghoul'))

# print(Dun)