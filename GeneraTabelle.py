from random import random, randint

def PrintTabella(tabella: list) -> None:
    '''Prints the tabella'''
    for row in tabella:
        for number in row:
            if number == 0: print(" -", end=" ")
            elif number < 10: print(f" {number}", end=" ")
            else: print(number, end=" ")
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

if __name__ == "__main__":
    main()