from random import random, randint
from PIL import Image, ImageDraw, ImageFont
import os
import os.path
import shutil
import subprocess

WIDTH = 900
HEIGHT = 300
CELL_WIDTH = WIDTH/9
CELL_HEIGHT = HEIGHT/3
FONT_SIZE = 40
IMG_OUT_NAME = "Tabella_"
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


    num_to_generate = 0
    while 1:
        num_to_generate_input = input("Quante tabelle si vogliono generare?(min: 1, max: 9): ")
        if len(num_to_generate_input) < 2 and ord(num_to_generate_input) >= 49 and ord(num_to_generate_input) <= 57:
            num_to_generate = int(num_to_generate_input)
            break
        else:
            print("Input non valido. Inserire un numero intero compreso tra 1 e 9.")

    shutil.rmtree(OUT_PATH)
    os.mkdir(OUT_PATH)

    for num in range(num_to_generate):
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
        DrawOnImage(tabella, num+1)

    print(f"I file generati sono presenti in: {OUT_PATH}")
    print("Apertura del percorso dove sono presenti i file in corso...")
    subprocess.Popen(r'explorer /open,"'+ OUT_PATH +'"')
    print("Fine.")

def DrawOnImage(tabella: list[list[int]], tabellaNumber: int) -> None:
    
    im = Image.open("Board.jpg")
    wr = ImageDraw.Draw(im)

    for i in range(len(tabella)):
        for j in range(len(tabella[0])):
            if tabella[i][j] != 0:
                coord = (j*CELL_WIDTH + (CELL_WIDTH/2)-FONT_SIZE, i*CELL_HEIGHT + (CELL_HEIGHT/2)-FONT_SIZE)
                wr.text(coord, str(tabella[i][j]), fill=(0,0,0), font=ImageFont.truetype("arial.ttf", 30))

    im.save(f"{OUT_PATH}{IMG_OUT_NAME}{tabellaNumber}.jpg")


def generateBoard():
    im = Image.new(mode="RGB", size=(WIDTH, HEIGHT), color=(255,255,255))
    draw = ImageDraw.Draw(im)

    # draw vertical lines
    for i in range(0, WIDTH, int(WIDTH/9)):
        draw.line([(i, 0), (i, HEIGHT)], width=2, fill=(0,0,0))

    # draw horizontal lines
    for i in range(0, HEIGHT, int(HEIGHT/3)):
        draw.line([(0, i), (WIDTH, i)], width=2, fill=(0,0,0))

    im.save("Board.jpg")

if __name__ == "__main__":
    main()