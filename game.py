'''
A rogue-like text-based adventure game.
'''

import time
from typing import Optional, Dict, Callable

from colorama import Style
from character import *
from dungeon import *


class InvalidException(Exception):
    pass


class Game:
    def __init__(self) -> None:
        # A list of the characters in the part
        self.__party: List[Character] = []
        # Current party gold
        self.__gold = 0
        # Starting dungeon
        self.__dungeons = [
            Dungeon("Dungeon Entrance", "The mouth of a giant cavern.  Danger lurks just past this door.")]
        # A reference to the current dungeon
        self.__current_location = self.__dungeons[0]
        # Add the commands
        self.__commands: Dict[str, (Callable, str)] = {}
        self.__setup_commands()
        # Start it up!
        self.__print_welcome()

    '''
    Adds the commands to the command dictionary.  This is a dictionary of strings keys that have
    function values.  This allows us to add/remove commands to the game easily by simply writing
    a new function and adding a dictionary key.
    '''

    def __setup_commands(self) -> None:
        self.__commands["help"] = (self.__show_help, "usage: help")
        self.__commands["?"] = (self.__show_help, "usage: ?")
        self.__commands["advance"] = (self.__advance, "usage: advance")
        self.__commands["retreat"] = (self.__retreat, "usage: retreat")
        self.__commands["attack"] = (self.__attack, "usage: player_name attack monster_name")
        self.__commands["heal"] = (self.__heal, "usage: priest_name heal player_name")
        self.__commands["party"] = (self.__party_stats, "usage: party")
        self.__commands["stats"] = (self.__stats, "usage: player_name stats")
        self.__commands["gold"] = (self.__see_gold, "usage: gold")
        self.__commands["take"] = (self.__take, "usage: player_name take item_name")
        self.__commands["inventory"] = (self.__player_inventory, "usage: player_name inventory")
        self.__commands["equip"] = (self.__equip, "usage: player_name equip weapon_name")
        self.__commands["remove"] = (self.__remove, "usage: player_name remove item_name")
        self.__commands["drop"] = (self.__drop, "usage: player_name drop item_name")
        self.__commands["monsters"] = (self.__show_monsters, "usage: monsters")
        self.__commands["leave"] = (self.__leave_dungeons, "usage: leave")
        self.__commands["exit"] = (self.__exit, "usage: exit")
        self.__commands["wear"] = (self.__wear, "usage: player_name wear item_name")

    '''
    A priest can heal a single party member for between 0 and 25 health.
    '''

    def __heal(self, priest: Priest, player: str, *args) -> None:
        # Not a priest? Can't heal then.
        if not isinstance(priest, Priest):
            Printer.alert(priest.name + "is not a priest!")
            raise InvalidException
        # Not a valid target?  Return.
        target = self.__in_party(player)
        if not target:
            Printer.alert(player + " is not in the party!")
            raise InvalidException
        # All checks out.  Call healing method.
        amt = priest.heal(target)
        if amt:
            Printer.alert(priest.name + " heals " + target.name + " for " + str(amt) + "hp!")

    '''
    End the game, if and only if the party is currently in the starting dungeon.
    '''

    def __exit(self, *args) -> None:
        # Not at the exit?  Can't leave.
        if self.__current_location != self.__dungeons[0]:
            Printer.alert("You cannot exit; you aren't at the dungeon exit!")
            raise InvalidException
        # Party dead.  Sadness.  Oh well, YOLO.
        if len(self.__party) == 0:
            Printer.alert("Your party has died in the dungeons.  Alas, there is no one left to mourn you.")
        # Good, maybe we got some gold.
        else:
            Printer.alert("You return with " + str(len(self.__party)) +
                          " members and " + str(self.__gold) + " gold!")
            Printer.alert("Well done, brave warriors!")
            exit(0)

    '''
    Flee back through all the prior dungeons to the exit.
    '''

    def __leave_dungeons(self, *args) -> None:
        while self.__current_location.prior:
            self.__retreat()

    '''
    Print a list of all monsters in the current location.
    '''

    def __show_monsters(self, *args):
        # Printer.info(self.__current_location.show_monsters())
        Printer.info(self.__current_location.__show_monsters__())

    '''
    Given a player and the name of an item, remove the item from usage.  If it
    is current weapon, or a piece of armor currently being worn, add it to the
    inventory.
    '''

    def __remove(self, player: Character, item_name: str, *args) -> None:
        item = self.__find_item(player, item_name)
        if item:
            player.inventory.append(item)

    '''
    Print the inventory for a give player.
    '''

    def __player_inventory(self, player: Character, *args) -> None:
        for item in player.inventory:
            Printer.info(item.__str__())

    '''
    Equipping a weapon adds the weapon's benefits to your stats.
    '''

    def __equip(self, player: Character, item_name: str, *args) -> None:
        # Weapon not in inventory?  Can't equip it.
        item = player.in_inventory(item_name)
        if item:
            if isinstance(item, Weapon):
                player.add_inventory(player.weapon)
                player.weapon = item
                player.inventory.remove(item)
                Printer.info("EQUIPPED " + str(item))
            # Not a weapon?  Can't equip it.
            else:
                Printer.alert("That isn't a weapon; you can't wield it.")
                raise InvalidException
        # Don't have that item?  Can't equip it.
        else:
            Printer.alert(player.name + " doesn't have that item in their inventory.")

    '''
    Wearing armor enhances defensive abilities.
    '''

    def __wear(self, player: Character, item_name: str, *args) -> None:
        item = player.in_inventory(item_name)
        if item:
            # print(type(item))
            if isinstance(item, Armor):
                for x in player.armor:
                    if x.name == item.name:
                        player.add_inventory(x)
                        player.armor.append(item)
                        player.inventory.remove(item)
                        Printer.info("WEARING " + str(item))
                        return
                player.armor.append(item)
                player.inventory.remove(item)
                Printer.info("WEARING " + str(item))

            else:
                Printer.alert("This isn't an armor; you can't wear it.")
                raise InvalidException
        else:
            Printer.alert(player.name + " doesn't have that item in their inventory.")

    '''
    Checks if Player is wielding or wearing the Item.
    '''

    def __find_item(self, player: Character, item_name, *args) -> Optional[Item]:
        item: Optional[Item] = None
        if player.weapon.name == item_name:
            item = player.weapon
            player.weapon = Weapon(("weapon", "Barehanded", 0, 0, 0))
        else:
            item = player.in_inventory(item_name)
            if item:
                player.inventory.remove(item)
        return item

    '''
    Remove the Item from the player's inventory (if exists) and add it to
    the room inventory.
    '''

    def __drop(self, player: Character, item_name, *args) -> None:
        item = self.__find_item(player, item_name)
        if item:
            self.__current_location.items.append(item)
        else:
            Printer.alert(player.name + " does not have that item.")

    '''
    Display player stats.
    '''

    def __stats(self, player: Character, *args) -> None:
        if player is not None:
            Printer.info(player)
        else:
            Printer.alert("You must specify which player you want stats for.")
            raise InvalidException

    '''
    Move to the next room.  If it doesn't exist, make it.
    '''

    def __advance(self, *args) -> None:
        if self.__current_location.next:
            self.__current_location = self.__current_location.next
        else:
            newDungeon = Dungeon("Dungeon Room", "A dark and eery place that radiates evil.")
            newDungeon.generate()
            self.__current_location.next = newDungeon
            newDungeon.prior = self.__current_location
            self.__current_location = newDungeon
        self.__show_monsters()

    '''
    Go back a room.  If at the entrance, you must exit instead.
    '''

    def __retreat(self, *args) -> None:
        if self.__current_location.prior:
            self.__current_location = self.__current_location.prior
        else:
            Printer.alert("You are at the entrance.  You must exit to leave.")

    '''
    Print the amount of gold in the party.
    '''

    def __see_gold(self, *args) -> None:
        Printer.info("Your party has " + str(self.__gold) + " gold!")

    '''
    See if the player is in the party.  Return them if they are.
    '''

    def __in_party(self, player: str, *args) -> Optional[Character]:
        warrior = None
        for character in self.__party:
            if character.name == player:
                warrior = character
                break
        return warrior

    '''
    If the item is in the room, add it to the inventory.
    '''

    def __take(self, player: Character, target: str, *args) -> None:
        item = None
        for object in self.__current_location.items:
            if object.description == target:
                item = object
                owned_item = player.in_inventory(item.description)
                if owned_item:
                    if item.description == owned_item.description:
                        Printer.alert("You already have a " + str(item) + " in your inventory.")
                        raise InvalidException
                player.add_inventory(object)
                self.__current_location.items.remove(object)
                break
        if not item:
            Printer.info("You must be seeing things.  There is no " + target + " here!")
            raise InvalidException

    '''
    Attempt to attack the target if it is in the room.
    '''

    def __attack(self, player: Character, target: str, *args) -> None:
        if isinstance(player, Priest):
            Printer.info("----- " + player.name + " refuses to break their vow! -----")
            raise InvalidException

        monster = self.__current_location.monster_in_dungeon(target)
        if not monster:
            Printer.info("There is no monster called " + target + " in this room!")
            raise InvalidException
        try:
            damage = monster.take_damage(player)
            Printer.alert("----- " + player.name + " attacks " + monster.name +
                          " for " + str(damage) + " damage! -----")
        except MonsterDeathException as ex:
            Printer.alert("!!!!!! - YES! " + ex.monster.name + " HAS FALLEN! - !!!!!!")
            Printer.info("From its remains you recover " +
                         str(ex.monster.gold) + " gold!")
            self.__gold = self.__gold + ex.monster.gold
            for item in ex.monster.inventory:
                self.__current_location.items.append(item)
            self.__current_location.monsters.remove(ex.monster)

    '''
    Now the monsters get to attack.
    '''

    def __monster_attack(self) -> None:
        try:
            for monster in self.__current_location.monsters:
                character = random.choice(self.__party)
                damage = character.take_damage(monster)
                Printer.alert("----- " + monster.name + " attacks "
                              + character.name + " for " + str(damage) +
                              " damage! -----")
        except CharacterDeathException as ex:
            Printer.alert("!!!!!! - NO! " + ex.character.name + " HAS FALLEN! - !!!!!!")
            self.__party.remove(ex.character)

    # removed name below from monster

    '''
    List all of the commands in the dictionary.
    '''

    def __show_help(self, *args) -> None:
        Printer.info("\nYour options are:\n")
        Printer.info("==========================\n")
        for key in self.__commands.keys():
            Printer.info('\t {:<10} {:<30}'.format(key, self.__commands[key][1]))

    '''
    Start it up.
    '''

    def __print_welcome(self) -> None:
        Printer.dialogue("WELCOME, TRAVELERS!")
        Printer.text("You hear the innkeeper say as your weary party enters the inn.")
        Printer.text("Many days you have been on the road making your way to this town,")
        Printer.text("as you have heard the stories of the precious gold in the nearby")
        Printer.text("dugeons.  After a night or two your party should be well-rested,")
        Printer.text("and ready to claim what other heroes died trying to earn.")
        print()
        Printer.text("What the other travelers don't know, is that your party is different.")
        Printer.text("For you have spent years discerning just the right makeup for a band")
        Printer.text("of warriors, such that you can not only enter the dungeons, but emerge")
        Printer.text("again with your sacks full of gold.")
        Printer.text("First, you have ")
        self.__party.append(self.__choose_player())
        Printer.dialogue("Ah yes, " +
                         self.__party[0].quick_info() +
                         "! They are a formidable foe indeed.")
        Printer.dialogue("But that's, not all - for I also see ")
        self.__party.append(self.__choose_player())
        Printer.dialogue(self.__party[1].quick_info() +
                         ". Few have crossed them and lived to tell the tale.  And then there is")
        self.__party.append(self.__choose_player())
        Printer.dialogue(self.__party[2].quick_info() +
                         ".  A more noble, and more loyal friend you could find nowhere.")
        Printer.dialogue("And finally, I notice in the corner")
        self.__party.append(self.__choose_player())
        Printer.dialogue(self.__party[3].quick_info() +
                         ".  Incredible!  The legends I have heard of that one shall never")
        Printer.dialogue("be forgotten.")
        print()
        Printer.dialogue("It is late.  Your party should try to sleep...")
        for i in range(0, 8):
            time.sleep(0.25)
            print(".", end='')
        print()
        Printer.info("You awake well rested.")
        self.__party_stats()

    '''
    Print party statistics.
    '''

    def __party_stats(self, *args) -> None:
        Printer.info("The current statistics of our players are as follows: ")
        for player in self.__party:
            Printer.info(player)

    '''
    Create the four party members.
    '''

    def __choose_player(self) -> Character:
        Printer.alert("(What is the name of this player?)")
        name = input()
        while True:
            Printer.info("Choose the class for this player: ")
            Printer.info("\t1. Bard - has healing abilities.")
            Printer.info("\t2. Tank - has extra defense.")
            Printer.info("\t3. DPS - specializes in attacking.")
            Printer.info("\t4. Priest - Blesses the party with increased luck.")
            Printer.info("")
            Printer.alert("Enter your choice (1-4)? ")
            try:
                cls = int(input())
                if cls not in (1, 2, 3, 4):
                    Printer.alert("That is not valid input.")
                    continue
                break
            except ValueError:
                Printer.alert("That is not valid input.")

        player: Optional[Character] = None
        if cls == 1:
            player = Bard(name)
        elif cls == 2:
            player = Tank(name)
        elif cls == 3:
            player = DPT(name)
        else:
            player = Priest(name)
        return player

    '''
    Play the game.
    '''

    def play(self) -> None:
        while (True):
            Printer.alert("Your party is in:\n")
            Printer.info(self.__current_location)
            cmd = input("What would you like to do? (help or ? for commands): ")
            toks = cmd.split(' ')
            toks = [x.rstrip("\n") for x in toks]
            action = toks[0]
            player = None
            if len(toks) > 1:
                action = toks[1]
                player = self.__in_party(toks[0])
                if not player:
                    Printer.alert("Have you hit your head? " + toks[0] + " is not in this party.")
                    continue
            if action in self.__commands:
                try:
                    self.__commands[action][0](player, ' '.join(toks[2:]))
                except InvalidException:
                    continue
            else:
                Printer.alert("\t>>>>> I don't know what that command means. <<<<<")
                continue
            if action not in ['stats', 'party', 'help', '?', 'monsters']:
                self.__monster_attack()


def main():
    g = Game()
    g.play()


if __name__ == '__main__':
    main()
    # c = Character('gordi')
    # print(c.total_defense)