# -*- coding: utf-8 -*-
import random
import json

def main() -> None:
    '''Main function'''
    alreadyRolled = [] #list to store the numbers already rolled
    
    #load json data
    smorfia = {}
    try:
        with open("Smorfia.json", "r", encoding="utf-8") as data:
            smorfia = json.load(data)
    except:
        print("Unable to read json file to load the Smorfia")
    
    #wait for user interaction before starting the game
    if input("Iniziare il gioco?(s/n): ") == "n": return
    
    #game loop
    while 1:
        n = 0
        #roll untill a not already rolled number comes out
        while 1:
            n = random.randint(1, 90)
            if n not in alreadyRolled:
                alreadyRolled.append(n)
                break
        
        printBoard(alreadyRolled) #print the board's current situation
        try:
            print("Numero estratto: " + str(n) + "; " + smorfia[str(n)]["napoletano"] + " (" + smorfia[str(n)]["italiano"] + ")") #print the smorfia and the equivalent meaning in italian
        except KeyError:
            print("Numero estratto: " + str(n))
        
        #if one of the below is true than the game will end
        if input("Altro numero?(s/n): ") == 'n' or len(alreadyRolled) == 90: break

    print("Tombola finita!")

def printBoard(ls: list) -> None:
    '''Prints the board's state'''
    count = 1
    greenFont = "\33[0;32;40m" #ANSI code for green text
    whiteFont = "\33[0;37;40m" #we could use the "colorama" module to do this in te future...
    print("\n########## TABELLONE #########")
    rows = 0
    for i in range(9):
        rows += 1
        cols = 0
        for j in range(10):
            cols += 1
            if cols == 6:
                print(" ", end="")
            if count in ls: #print the number in green
                print(greenFont, end="") #set font color to green in the terminal
                
                if count < 10: print(" " + str(count) + " ", end="") #add an extra space at the beginning
                else: print(str(count) + " ", end="")

                print(whiteFont, end="") #set font color back to white
                count += 1
            else:
                if count < 10: print(" " + str(count) + " ", end="") #add an extra space at the beginning
                else: print(str(count) + " ", end="")
                count += 1
        if rows == 3:
            print() #add an extra blank line
            rows = 0
        print()
    
if __name__ == "__main__":
    main()
