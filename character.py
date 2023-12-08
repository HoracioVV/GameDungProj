import datetime
import random

from abc import *
from typing import Optional


from item import *
from printer import Printer


class CharacterDeathException(Exception):
    def __init__(self, st, character) -> None:
        super().__init__(st)
        self.character = character

class MonsterDeathException(Exception):
    def __init__(self, st, monster) -> None:
        super().__init__(st)
        self.monster = monster

class CharacterOverweightException(Exception):
    def __init__(self, st, weight) -> None:
        super().__init__(st)
        self.weight = weight


class Character(ABC):
    def __init__(self, name):
        self.__name = name
        self.__health = random.randint(50, 100)
        self.__base_attack = random.randint(5, 20)
        self.__base_defense = random.randint(5, 10)
        self.__luck = random.randint(1, 100)
        self.__inventory = []
        self.__armor = []
        self.__weapon = Weapon(("weapon", "Barehanded", 1, 0, 0))
        self.__weapon.condition[0] = 'Normal'

    @property
    def name(self):
        return self.__name
        # raise AttributeError

    @name.setter
    def name(self, name):
        self.__name = name
    # optional: ask wheather or not we need the property or just setter




    @property
    def health(self):
        return self.__health


    @health.setter
    def health(self, health):

        self.__health = health
        if self.__health <= 0:
            raise CharacterDeathException('character got killed', self)





    @property
    def inventory(self):
        return self.__inventory




    @property
    def armor(self):
        return self.__armor

    @armor.setter
    def armor(self, armor):
        self.__armor = armor

        if armor in self.__armor:
            self.__inventory.append(armor)
        else:
            self.__armor.append(armor)


    @property
    def weapon(self):
        return self.__weapon

    @weapon.setter
    def weapon(self, weapon):
        self.__weapon = weapon





    @property
    def base_attack(self):
        return self.__base_attack

    @base_attack.setter
    def base_attack(self, base_attack):
        self.__base_attack = base_attack






    @property
    def base_defense(self):
        return self.__base_defense

    @base_defense.setter
    def base_defense(self, base_defense):
        self.__base_defense = base_defense





    @property
    def total_attack(self):
        return self.base_attack + self.weapon.added_attack



    @property
    def total_defense(self):
        # baseD = self.base_defense
        # addedD = Armor.added_defense
        # listofD = [baseD, addedD]
        # totalD = sum(listofD)
        total = 0
        for armor in self.__armor:
            total += armor.added_defense
        return self.base_defense + total

    # def __init__(self, name):
    #     self.__name = name
    #     self.__health = random.randint(50, 100)
    #     self.__base_attack = random.randint(5, 20)
    #     self.__base_defense = random.randint(5, 10)
    #     self.__luck = random.randint(1, 100)
    #     self.__inventory = []
    #     self.__armor = []
    #     self.__weapon = Weapon(("weapon", "Barehanded", 1, 0, 0))
    #     self.__weapon.condition[0] = 'Normal'

    def add_inventory(self, item) -> None:
        self.__inventory.append(item)
        totalweight = 0
        # tankweight = Tank()

        # for x in self.__inventory:
        #     totalweight += x[-1]
        #
        # if totalweight > Character:
        #     raise CharacterOverweightException

    def quick_info(self) -> str:
        return self.__name + self.__class__.__name__


    def in_inventory(self, item_description) -> Optional[Item]:

        for x in self.__inventory:
            if x.description == item_description:
                return x
            else:
                return None


    def wearing(self, item_description) -> Optional[Armor]:
        for x in self.__armor:
            if x == item_description:
                return x
            else:
                return None



    def take_damage(self, enemy) -> int:
        randomroll = random.randint(1, 100)
        edamage = 0
        if self.__luck < randomroll:
            return edamage
        elif self.__luck > randomroll:
            # e_base_attack = enemy.base_attack
            # gg = Monster.weapon
            # go = gg.
            edamage = (enemy.total_attack - self.total_defense)
            # edamage = enemy.base_attack - self.total_defense
            # edamage = Monster.total_attack - self.total_defense

            if edamage <= 0:
                return edamage
            else:
                self.health -= edamage
                # if self.health <= 0:
                #     raise CharacterDeathException
                return edamage

        # if self.__luck < randomroll:
        #     return self.__health



    def __str__(self) -> str:
        id = ''
        for x in self.__inventory:
            id += x.itemdesc

        ad = ''
        for y in self.__armor:
            ad += y.itemdesc

        return (f'|Name|: {self.__name}\n|Health|: {self.__health}\n|Weapon name/condition|: {self.__weapon}\n'
                f'|Armor|: {ad}\n|Inventory|: {id}\n'
                f'|Class|: {self.__class__.__name__}\n|Total attack|: {self.total_attack}\n'
                f'|Total defense|: {self.total_defense}\n|Luck|: {self.__luck}\n')





# TODO: look over Priest class and be sure you understand it
class Priest(Character):
    def __init__(self, name) -> None:
        super().__init__(name)
        self.last_healing = datetime.datetime.now() - datetime.timedelta(minutes=2)
        self.weight = 28



    def take_damage(self, enemy) -> int:
        # print(enemy)
        Printer.info(enemy.name + " senses the holiness of " + self.name + " and chooses not to attack!")
        return 0

    # removed name from enemy above

    def heal(self, target) -> Optional[int]:
        if datetime.datetime.now() - self.last_healing < datetime.timedelta(minutes = 2):
            Printer.alert(self.name + " hasn't recovered from the last healing!")
            return None
        self.last_healing = datetime.datetime.now()
        amt = random.randint(0, 25)
        target.health += amt
        return amt



# TODO: implement Tank class

class Tank(Character):
    def __init__(self, name) -> None:
        super().__init__(name)
        self.base_defense = self.base_defense * 1.2
        self.weight = 8



# TODO: implement DPT class

class DPT(Character):
    def __init__(self, name) -> None:
        super().__init__(name)
        self.base_attack = self.base_attack * 90
        self.weight = 5


# TODO: implement Bard class

class Bard(Character):
    def __init__(self, name) -> None:
        super().__init__(name)
        bd = self.base_attack * 1.2
        self.base_attack = bd
        # self.base_attack = self.base_attack * 1.2
        self.last_defense = datetime.datetime.now() - datetime.timedelta(minutes=2)
        self.weight = 17

    def boosted_defense(self, target) -> Optional[int]:
        if datetime.datetime.now() - self.last_defense < datetime.timedelta(minutes=2):
            Printer.alert(self.name + " hasn't fixed armorrrr!")
            return None
        self.last_defense = datetime.datetime.now()
        incr = random.randint(0, 75)
        target.base_defense += incr
        return incr

# TODO: implement Monster class

class Monster(Character):
    @property
    def gold(self):
        return self.__gold

    @property
    def health(self):

        # return self.health

        return Character.health.fget(self)  # if broken, add underscores

    @health.setter
    def health(self, health):
        if health <= 0:
            raise MonsterDeathException('monster got killed', self)

        Character.health.fset(self, health)

        # if health <= 0:
        #     raise MonsterDeathException

        # super().health = health
        # if super().health <= 0:
        #     raise MonsterDeathException
    def __init__(self, name) -> None:
        super().__init__(name)
        self.health = self.health // 2
        self.base_attack = self.base_attack // 4
        self.__gold = random.randint(0, 10)
        self.description_inventory = []
        self.randominteger = random.randint(0, 1)
        # if self.randominteger == 1:
        #     self.monster_inventory.append(random.choice(self.armor.ITEMS))

        if self.randominteger == 1:
            # self.monster_inventory = self.inventory.append(random.choice(Item.ITEMS))
            randitem = random.choice(Item.ITEMS)
            randitemtype = randitem[0]
            if randitemtype == 'armor':
                AR = Armor(randitem)
                self.inventory.append(AR)
            elif randitemtype == 'weapon':
                WP = Weapon(randitem)
                self.inventory.append(WP)
            self.description_inventory.append(randitem)


        # if self.__health <= 0:
        #     raise MonsterDeathException

    def __str__(self) -> str:
        return f'{Character.__str__(self)}|Gold|: {self.__gold}\n'

        # self.__str__() + f' {self.gold}'

# sw = Item.name
# print(sw)

