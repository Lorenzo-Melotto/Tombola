from utils import *
from RewardState import RewardState
from Reward import Reward
import colorama
from colorama import Fore
colorama.init(autoreset=True)

class Board:
  board: list[list[RewardState]]
  check_ambo: list[list[RewardState]]
  check_terno: list[list[RewardState]]
  check_quaterna: list[list[RewardState]]
  check_tombola: list[list[RewardState]]

  ambo_won: RewardState
  terno_won: RewardState
  quaterna_won: RewardState
  tombola_won: RewardState
  
  def __init__(self):
    self.board = [[n+off*10 for n in range(1,11)] for off in range (9)] # game board

    self.check_ambo = [[RewardState.NOT_WON for _ in range(3)] for _ in range(6)]
    self.check_terno = [[RewardState.NOT_WON for _ in range(3)] for _ in range(6)]
    self.check_quaterna = [[RewardState.NOT_WON for _ in range(3)] for _ in range(6)]
    self.check_tombola = [[RewardState.NOT_WON for _ in range(3)] for _ in range(6)]

    self.ambo_won = RewardState.NOT_WON
    self.terno_won = RewardState.NOT_WON
    self.quaterna_won = RewardState.NOT_WON
    self.tombola_won = RewardState.NOT_WON

  def printBoard(self, alreadyRolled: list[int]) -> None:
    '''Prints the board's state'''
    count = 1
    print(f"\n########## {getRainbowString('TABELLONE')} #########")
    rows = 0
    for i in range(9):
        rows += 1
        cols = 0
        for j in range(10):
            cols += 1
            if cols == 6:
                print(" ", end="")
            if count in alreadyRolled: #print the number in green
                
                if count < 10: print(f"{Fore.GREEN} {str(count)} ", end="") #add an extra space at the beginning
                else: print(f"{Fore.GREEN}{str(count)} ", end="")

                count += 1
            else:
                if count < 10: print(f" {str(count)} ", end="") #add an extra space at the beginning
                else: print(f"{str(count)} ", end="")
                count += 1
        if rows == 3:
            print() #add an extra blank line
            rows = 0
        print()
    
  def checkBoard(self, alreadyRolled: list[int]) -> None:
    # prima cartella
    for i in range(3):
      count = 0
      for j in range(5):
          if self.board[i][j] in alreadyRolled:
              count += 1
      self._checkReward(count, i, 0)

    # seconda cartella
    for i in range(3):
      count = 0
      for j in range(5, 10):
          if self.board[i][j] in alreadyRolled:
              count += 1
      self._checkReward(count, i, 1)

    # terza cartella
    for i in range(3, 6):
      count = 0
      for j in range(5):
          if self.board[i][j] in alreadyRolled:
              count += 1
      self._checkReward(count, i, 2)

    # quarta cartella
    for i in range(3, 6):
      count = 0
      for j in range(5, 10):
          if self.board[i][j] in alreadyRolled:
              count += 1
      self._checkReward(count, i, 3)

    # quinta cartella
    for i in range(6, 9):
      count = 0
      for j in range(5):
          if self.board[i][j] in alreadyRolled:
              count += 1
      self._checkReward(count, i, 4)

    # sesta cartella
    for i in range(6, 9):
      count = 0
      for j in range(5, 10):
          if self.board[i][j] in alreadyRolled:
              count += 1
      self._checkReward(count, i, 5)

  def _checkReward(self, count: int, row: int, cartella: int) -> None:
    if count == Reward.AMBO.value:
      if self.ambo_won == RewardState.NOT_WON:
        print(f"{getRainbowString('AMBO')}! Cartella n°{cartella+1}, riga n°{(row+1)%3}")
    if count == Reward.TERNO.value:
      if self.terno_won == RewardState.NOT_WON:
        print(f"{getRainbowString('TERNO')}! Cartella n°{cartella+1}, riga n°{(row+1)%3}")
    if count == Reward.QUATERNA.value:
      if self.quaterna_won == RewardState.NOT_WON:
        print(f"{getRainbowString('QUATERNA')}! Cartella n°{cartella+1}, riga n°{(row+1)%3}")
    if count == Reward.TOMBOLA.value:
      if self.tombola_won == RewardState.NOT_WON:
        print(f"{getRainbowString('TOMBOLA')}! Cartella n°{cartella+1}, riga n°{(row+1)%3}")