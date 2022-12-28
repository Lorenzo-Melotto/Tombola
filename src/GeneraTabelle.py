from random import randint
from PIL import Image, ImageDraw, ImageFont
import os
import os.path
import shutil
import subprocess
import time
from datetime import datetime

WIDTH = 900
HEIGHT = 300
OFFSET_Y = 50
V_LINES_NUM = 9
H_LINES_NUM = 3
CELL_WIDTH = WIDTH/9
CELL_HEIGHT = HEIGHT/3
FONT_SIZE = 30
SMALLER_FONT_SIZE = 20
IMG_OUT_NAME = "Tabelle"
OUT_PATH = f"{os.path.abspath(os.path.curdir)}{os.path.sep}images_out{os.path.sep}"

def PrintTabella(tabella: list) -> None:
    '''Prints the tabella'''
    for row in tabella:
        for number in row:
            if number == 0: print(" -", end=" ")
            elif number < 10: print(f" {number}", end=" ")
            else: print(number, end=" ")
        print("")
    print("")

def PickNumber(lowerRange: int, upperRange: int, alreadyRolled: set) -> int:
    '''Generates a valid random number between the range [lowerRange, upperRange]'''
    while True:
        num = randint(lowerRange, upperRange)
        if num not in alreadyRolled: break
    alreadyRolled.add(num)
    return num

def main() -> None:
    '''Main function'''
    playerName = input("Nome del giocatore: ")

    # reading how many boards the user wants to buy
    numToGenerate = 0
    while 1:
        num_to_generate_input = input("Quante tabelle si vogliono comprare?(min: 1, max: 9): ")
        if len(num_to_generate_input) < 2 and ord(num_to_generate_input) >= 49 and ord(num_to_generate_input) <= 57:
            numToGenerate = int(num_to_generate_input)
            break
        else:
            print("Input non valido. Inserire un numero intero compreso tra 1 e 9.")

    #reading the boards number
    tabelle = []
    for _ in range(numToGenerate):
        n = 0
        while 1:
            gotError = False
            userInput = input("Numero della cartella che si vuole acquistare: ")
            try:
                n = int(userInput)
            except Exception:
                # checking that the user inputted a number
                print("Inserire un numero intero!")
                gotError = True
            if not gotError: 
                # checking that the user inputted a number between 1 and 90
                if n > 0 and n <= 90:
                    if n in tabelle:
                        print(f"Tabella #{n} già presa!")
                    else:
                        break
                else:
                    print("Inserire un numero intero compreso tra 1 e 90!")
        tabelle.append(n)

    today = datetime.now()
    formattedToday = today.strftime("%d/%m/%Y %H:%M")

    if(os.path.isdir(OUT_PATH)):
        shutil.rmtree(OUT_PATH)

    os.mkdir(OUT_PATH)

    tabelleGenerate = []
    for num in range(numToGenerate):
        tabella = [[0 for _ in range(9)] for _ in range(3)]
        alreadyRolled = set()
        for i in range(3):
            spots = [0 for _ in range(9)]
            chosenSpots = set()
            # generate the random spots in the current row
            for _ in range(5):
                while True:
                    spot = randint(0, 8)
                    if spot not in chosenSpots: break
                spots[spot] = 1
                chosenSpots.add(spot)
            
            # if the spot is set with 1, pick the number to put in the tabella
            if spots[0] == 1:
                tabella[i][0] = PickNumber(1, 9, alreadyRolled)
            if spots[1] == 1:
                tabella[i][1] = PickNumber(10, 19, alreadyRolled)
            if spots[2] == 1:
                tabella[i][2] = PickNumber(20, 29, alreadyRolled)
            if spots[3] == 1:
                tabella[i][3] = PickNumber(30, 39, alreadyRolled)
            if spots[4] == 1:
                tabella[i][4] = PickNumber(40, 49, alreadyRolled)
            if spots[5] == 1:
                tabella[i][5] = PickNumber(50, 59, alreadyRolled)
            if spots[6] == 1:
                tabella[i][6] = PickNumber(60, 69, alreadyRolled)
            if spots[7] == 1:
                tabella[i][7] = PickNumber(70, 79, alreadyRolled)
            if spots[8] == 1:
                tabella[i][8] = PickNumber(80, 90, alreadyRolled)

        # check if the board number is in the board
        found = False
        col = tabelle[num] // 10
        for i in range(3):
            if col == 9: col = col - 1
            if tabella[i][col] == tabelle[num]:
                found = True
                break
        
        # if it's not in the board, forcefully add it
        if not found:
            randRow = randint(0, 2)
            tabella[randRow][col] = tabelle[num]
            if tabella[randRow].count(0) != 4:
                while 1:
                    randElem = randint(0, 8)
                    if tabella[randRow][randElem] != tabelle[num] and tabella[randRow][randElem] != 0:
                        tabella[randRow][randElem] = 0
                        break

        PrintTabella(tabella)
        tabelleGenerate.append(tabella)
        
    DrawTabelle(tabelleGenerate, tabelle, playerName, formattedToday)

    print(f"L'immagine generata si trova in: {OUT_PATH}")
    print("Apertura del percorso dove sono presenti i file in corso...")
    time.sleep(0.5)
    subprocess.Popen(r'explorer /open,"'+ OUT_PATH +'"')
    print("Fine.")

def DrawTabelle(tabelleGenerate: list[list[int]], tabelle: list[int], playerName: str, timeDate: str) -> None:
    arial_30 = ImageFont.truetype("arial.ttf", FONT_SIZE)
    arial_20 = ImageFont.truetype("arial.ttf", SMALLER_FONT_SIZE)
    numTabelle = len(tabelleGenerate)

    imOut = Image.new(mode="RGB", size=(WIDTH, (HEIGHT+OFFSET_Y)*numTabelle), color=(255,255,255))
    imBoard = Image.open("Board.jpg")

    # pasting the board inside the new image a number of times equal to the number of boards
    for i in range(len(tabelleGenerate)):
        imOut.paste(imBoard, (0, (HEIGHT+OFFSET_Y)*i))

    wr = ImageDraw.Draw(imOut)
    for n, tabella in enumerate(tabelleGenerate):
        for i in range(len(tabella)):
            for j in range(len(tabella[0])):
                if tabella[i][j] != 0:
                    coord = coord = (j*CELL_WIDTH + (CELL_WIDTH/2)-(FONT_SIZE/2), (i*CELL_HEIGHT + (CELL_HEIGHT/2)-(FONT_SIZE/2)-(OFFSET_Y/2))+n*(HEIGHT+OFFSET_Y))
                    num = str(tabella[i][j])
                    if len(num) == 1: num = f" {num}"
                    wr.text(coord, num, fill=(0,0,0), font=arial_30)

        wr.text((10, (HEIGHT+(OFFSET_Y/2)-(SMALLER_FONT_SIZE/2))+n*(HEIGHT+OFFSET_Y)), \
                f"Tabella #{tabelle[n]} {timeDate} ({playerName})", \
                fill=(0,0,0), \
                font=arial_20)

    imOut.save(f"{OUT_PATH}{playerName}_{IMG_OUT_NAME}.jpg")

def mainOld() -> None:
    '''Main function'''
    playerName = input("Nome del giocatore: ")

    # reading how many boards the user wants to buy
    numToGenerate = 0
    while 1:
        num_to_generate_input = input("Quante tabelle si vogliono comprare?(min: 1, max: 9): ")
        if len(num_to_generate_input) < 2 and ord(num_to_generate_input) >= 49 and ord(num_to_generate_input) <= 57:
            numToGenerate = int(num_to_generate_input)
            break
        else:
            print("Input non valido. Inserire un numero intero compreso tra 1 e 9.")

    #reading the boards number
    tabelle = []
    for _ in range(numToGenerate):
        n = 0
        while 1:
            gotError = False
            userInput = input("Numero della cartella che si vuole acquistare: ")
            try:
                n = int(userInput)
            except Exception:
                # checking that the user inputted a number
                print("Inserire un numero intero!")
                gotError = True
            if not gotError: 
                # checking that the user inputted a number between 1 and 90
                if n > 0 and n <= 90:
                    break
                else:
                    print("Inserire un numero intero compreso tra 1 e 90!")
        tabelle.append(n)

    today = datetime.now()
    formattedToday = today.strftime("%d/%m/%Y %H:%M")

    if os.path.isdir(OUT_PATH):
        shutil.rmtree(OUT_PATH)
    
    os.mkdir(OUT_PATH)

    for num in range(numToGenerate):
        tabella = [[0 for _ in range(9)] for _ in range(3)]
        alreadyRolled = set()
        for i in range(3):
            spots = [0 for _ in range(9)]
            chosenSpots = set()
            # generate the random spots in the current row
            for _ in range(5):
                while True:
                    spot = randint(0, 8)
                    if spot not in chosenSpots: break
                spots[spot] = 1
                chosenSpots.add(spot)
            
            # if the spot is set with 1, pick the number to put in the tabella
            if spots[0] == 1:
                tabella[i][0] = PickNumber(1, 9, alreadyRolled)
            if spots[1] == 1:
                tabella[i][1] = PickNumber(10, 19, alreadyRolled)
            if spots[2] == 1:
                tabella[i][2] = PickNumber(20, 29, alreadyRolled)
            if spots[3] == 1:
                tabella[i][3] = PickNumber(30, 39, alreadyRolled)
            if spots[4] == 1:
                tabella[i][4] = PickNumber(40, 49, alreadyRolled)
            if spots[5] == 1:
                tabella[i][5] = PickNumber(50, 59, alreadyRolled)
            if spots[6] == 1:
                tabella[i][6] = PickNumber(60, 69, alreadyRolled)
            if spots[7] == 1:
                tabella[i][7] = PickNumber(70, 79, alreadyRolled)
            if spots[8] == 1:
                tabella[i][8] = PickNumber(80, 90, alreadyRolled)

        PrintTabella(tabella)
        DrawOnImage(tabella, tabelle[num], playerName, formattedToday)

    print(f"I file generati sono presenti in: {OUT_PATH}")
    print("Apertura del percorso dove sono presenti i file in corso...")
    time.sleep(0.5)
    subprocess.Popen(r'explorer /open,"'+ OUT_PATH +'"')
    print("Fine.")

def DrawOnImage(tabella: list[list[int]], tabellaNumber: int, playerName: str, timeDate: str) -> None:    
    im = Image.open("Board.jpg")
    wr = ImageDraw.Draw(im)
    arial_30 = ImageFont.truetype("arial.ttf", FONT_SIZE)
    arial_20 = ImageFont.truetype("arial.ttf", SMALLER_FONT_SIZE)

    # write the numbers on the image
    for i in range(len(tabella)):
        for j in range(len(tabella[0])):
            if tabella[i][j] != 0:
                coord = (j*CELL_WIDTH + (CELL_WIDTH/2)-(FONT_SIZE/2), i*CELL_HEIGHT + (CELL_HEIGHT/2)-(FONT_SIZE/2)-(OFFSET_Y/2))
                num = str(tabella[i][j])
                if len(num) == 1: num = f" {num}"
                wr.text(coord, num, fill=(0,0,0), font=arial_30)

    # writing the board number, time and player name
    wr.text((10, HEIGHT+(OFFSET_Y/2)-(SMALLER_FONT_SIZE/2)), \
            f"Tabella #{tabellaNumber} {timeDate} ({playerName})", \
            fill=(0,0,0), \
            font=arial_20)

    # saving the image
    im.save(f"{OUT_PATH}{playerName}_{IMG_OUT_NAME}{tabellaNumber}.jpg")

def generateBoard():
    im = Image.new(mode="RGB", size=(WIDTH, HEIGHT+OFFSET_Y), color=(255,255,255))
    draw = ImageDraw.Draw(im)

    # draw vertical lines
    for i in range(0, int(WIDTH + WIDTH/V_LINES_NUM), int(WIDTH/V_LINES_NUM)):
        draw.line([(i, 0), (i, HEIGHT)], width=2, fill=(0,0,0))

    # draw horizontal lines
    for i in range(0, int(HEIGHT + HEIGHT/H_LINES_NUM), int(HEIGHT/H_LINES_NUM)):
        draw.line([(0, i), (WIDTH, i)], width=2, fill=(0,0,0))

    im.save("Board3.jpg")

if __name__ == "__main__":
    main()
    # generateBoard()