#! /usr/bin/python
from sys import exit

from colorama import Style

import actions
import actions.decode
import actions.generate
import helpers.printing as printing

if __name__ == "__main__":
    print(f"{Style.BRIGHT}Which action would you like to do?")
    print(f" 0. Generate Signal\n 1. Decode Signal")
    
    action = printing.prompt("Action")
    try:
        action = int(action)
    except ValueError:
        printing.notice("ERROR", "You must input an integer!")
        exit(1)
    
    if action < 0 or action > 1:
        printing.notice("ERROR", f"Action {action} does not exit!")
        exit(1)
    
    match action:
        case 0:
            actions.generate.start()
        case 1:
            actions.decode.start()