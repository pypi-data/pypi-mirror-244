from colorama import init, Fore


class User:
    def __init__(self):
        init()
        self.clear = "\033c"
        self.red = Fore.RED
        self.blue = Fore.BLUE
        self.green = Fore.GREEN
        self.reset = Fore.RESET

    def Ctext(self, colour, text):
        print(f"{colour}{text}{self.reset}\n")

    def clear(self):
        print(self.clear)

    def Choice(self, text: str, options: list):
        check = [i for i in range(1, len(options) + 1)]

        while True:
            self.Ctext(self.blue, f"{text}")
            for i, option in enumerate(options):
                print(f"({i + 1}) {option}")
            choice = input("\nInput: ")
            if choice.isnumeric():
                if int(choice) in check:
                    return int(choice)
                else:
                    self.Ctext(self.red, f"{self.clear}Input must be one of the options (e.g. 1).")
                    continue
            else:
                self.Ctext(self.red, f"{self.clear}Input must be an integer.")
                continue
