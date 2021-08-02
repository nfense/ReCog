from colorama import init
init()

RESET = "\u001b[0m"

RED = "\u001b[31m"
GREEN = "\u001b[32m"
YELLOW = "\u001b[33m"
BLUE = "\u001b[34m"
MAGENTA = "\u001b[35m"
CYAN = "\u001b[36m"
WHITE = "\u001b[37m"

B_RED = "\u001b[31;1m"
B_GREEN = "\u001b[32;1m"
B_YELLOW = "\u001b[33;1m"
B_BLUE = "\u001b[34;1m"
B_MAGENTA = "\u001b[35;1m"
B_CYAN = "\u001b[36;1m"
B_WHITE = "\u001b[37;1m"

BOLD = "\u001b[1m"
UNDERLINE = "\u001b[4m"
REVERSED = "\u001b[7m"


class Logger:
    def print(self, text):
        print(text
              .replace("{red}", RED)
              .replace("{green}", GREEN)
              .replace("{yellow}", YELLOW)
              .replace("{blue}", BLUE)
              .replace("{magenta}", MAGENTA)
              .replace("{cyan}", CYAN)
              .replace("{white}", WHITE)
              .replace("{b:red}", B_RED)
              .replace("{b:green}", B_GREEN)
              .replace("{b:yellow}", B_YELLOW)
              .replace("{b:blue}", B_BLUE)
              .replace("{b:magenta}", B_MAGENTA)
              .replace("{b:cyan}", B_CYAN)
              .replace("{b:white}", B_WHITE)
              .replace("{reset}", RESET)
              .replace("{bold}", BOLD)
              .replace("{reversed}", REVERSED)
              .replace("{underline}", UNDERLINE)
              + RESET)

    def debug(self, text):
        self.print("{bold}{magenta}DBG {reset}" + text)

    def log(self, text):
        self.print("{bold}{cyan}LOG {reset}" + text)

    def warn(self, text):
        self.print("{bold}{yellow}WRN {reset}" + text)

    def critic(self, text):
        self.print("{bold}{red}CRT {reset}" + text)

    def success(self, text):
        self.print("{bold}{green}SUC {reset}" + text)
