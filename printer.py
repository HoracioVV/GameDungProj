from colorama import Back, Fore, Style

class Printer:
    @staticmethod
    def info(message) -> None:
        print( Back.BLACK + Fore.LIGHTWHITE_EX + message.__str__() )

    @staticmethod
    def alert(message) -> None:
        print( Back.BLACK + Fore.LIGHTRED_EX + message.__str__() )

    @staticmethod
    def dialogue(message) -> None:
        print( Fore.BLACK + Back.LIGHTGREEN_EX + '"' + message.__str__() + '"')

    @staticmethod
    def text(message) -> None:
        print( Back.BLACK + Fore.LIGHTWHITE_EX + message.__str__() )