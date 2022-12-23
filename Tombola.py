# -*- coding: utf-8 -*-
import random
import json
import os
import colorama
from colorama import Fore
colorama.init(autoreset=True)
from utils import *
from Board import *

title = """

 /$$$$$$$  /$$     /$$ /$$$$$$$$ /$$$$$$  /$$      /$$ /$$$$$$$   /$$$$$$  /$$        /$$$$$$ 
| $$__  $$|  $$   /$$/|__  $$__//$$__  $$| $$$    /$$$| $$__  $$ /$$__  $$| $$       /$$__  $$
| $$  \ $$ \  $$ /$$/    | $$  | $$  \ $$| $$$$  /$$$$| $$  \ $$| $$  \ $$| $$      | $$  \ $$
| $$$$$$$/  \  $$$$/     | $$  | $$  | $$| $$ $$/$$ $$| $$$$$$$ | $$  | $$| $$      | $$$$$$$$
| $$____/    \  $$/      | $$  | $$  | $$| $$  $$$| $$| $$__  $$| $$  | $$| $$      | $$__  $$
| $$          | $$       | $$  | $$  | $$| $$\  $ | $$| $$  \ $$| $$  | $$| $$      | $$  | $$
| $$          | $$       | $$  |  $$$$$$/| $$ \/  | $$| $$$$$$$/|  $$$$$$/| $$$$$$$$| $$  | $$
|__/          |__/       |__/   \______/ |__/     |__/|_______/  \______/ |________/|__/  |__/
                                                                                              
                                                                                              
                                                                                              

"""

def printMenu() -> str:
    valid_options = ["1", "2", "3"]
    while 1:
        print("Azioni disponibili: \n" +
                "1) Estrai un nuovo numero; \n" +
                "2) Assegna vittoria; \n" +
                "3) Termina il gioco. \n" +
                "Scelta: ", end="")
        res = input()
        if res in ["1", "2", "3"]:
            return res
        else:
            print("Scelta non valida.")

def updateVittorie(board: Board) -> None:
    res = None
    while 1:
        print("Cosa è stato vinto?\n"+
            "1) Ambo;\n" +
            "2) Terno;\n" +
            "3) Quaterna;\n" +
            "4) Tombola.\n" +
        "Scelta: ", end="")
        res = input()
        if res in ["1", "2", "3", "4"]:
            break
        else:
            print("Scelta non valida.")
    who = None
    while 1:
        print("Chi ha fatto ambo?\n"+
            "1) Io;\n"+
            "2) Un altro giocatore.\n"+
        "Scelta: ", end="")
        who = input()
        if who in ["1", "2"]:
            break
        else:
            print("Scelta non valida.")

    state = RewardState.WON_BY_ME if who == "1" else RewardState.WON_BY_OTHERS
    if res == "1":
        board.ambo_won = state
    elif res == "2":
        board.terno_won = state
    elif res == "3":
        board.quaterna_won = state
    elif res == "4":
        board.tombola_won = state

def main() -> None:
    '''Main function'''
    clearScreen()
    print(f"{getMultilineRainbowString(title)}")

    alreadyRolled = [] #list to store the numbers already rolled
    board = Board() #board initialization
    
    #load json data
    smorfia = {}
    try:
        with open("Smorfia.json", "r", encoding="utf-8") as data:
            smorfia = json.load(data)
    except:
        print("Unable to read json file to load the Smorfia")
    
    #wait for user interaction before starting the game
    if input("Iniziare il gioco?([s]/n): ") == "n": return
    
    #game loop
    while 1:
        n = 0
        #roll untill a not already rolled number comes out
        while 1:
            n = random.randint(1, 90)
            if n not in alreadyRolled:
                alreadyRolled.append(n)
                break

        board.printBoard(alreadyRolled) #print the board's current state
        board.checkBoard(alreadyRolled) #check if the board has won
        
        #print the smorfia and the equivalent meaning in italian
        try:
            print("Numero estratto: " + str(n) + "; " + smorfia[str(n)]["napoletano"] + " (" + smorfia[str(n)]["italiano"] + ")")
        except KeyError:
            print("Numero estratto: " + str(n))

        # exit when all the numbers have been rolled
        if len(alreadyRolled) == 90: break

        res = printMenu()
        if   res == "1": continue
        elif res == "2": updateVittorie(board)
        elif res == "3": break

    print("Tombola finita!")

if __name__ == "__main__":
    main()
