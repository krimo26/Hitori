#ESERCIZIO 6.7 HITORI, INIZIO

from boardgame import abstract, BoardGame, print_game, console_play
from boardgamegui import gui_play
import random
import copy

class Hitori(BoardGame):
    def __init__(self,w,h):
        self._w = w
        self._h = h
        

        self._board = [[random.randint(1,w),False,False] for i in range(0,w*h)]
        #OGNI VALORE E' COMPOSTO DA [CIFRA, ANNERIMENTO, SEGNO]
        self._noted = copy.deepcopy(self._board)
        

    def cols(self):
        return self._w

    def rows(self):
        return self._h

    def finished(self):
        for x in self._rows:
            for y in self._cols:
                if self._noted[y*self._w + x][1]== False and self._noted.count([y*self._w + x][0]) > 1:
                    return False

    def message(self):
        pass
        
    def play_at(self,x,y):
        self._noted[y*self._w + x][1] = not self._noted[y*self._w + x][1]
        self._noted[y*self._w + x][2] = False

        #CONTROLLO PER ANNERIRE

    def flag_at(self,x,y):
        self._noted[y*self._w + x][2] = not self._noted[y*self._w + x][2]
        self._noted[y*self._w + x][1] = False

        #CONTROLLO PER SEGNARE

    def value_at(self,x,y):
        if self._noted[y*self._w + x][1] == True:
            return str(self._noted[y*self._w + x][0]) + "#"
        elif self._noted[y*self._w + x][2] == True:
            return str(self._noted[y*self._w + x][0]) + "!"
        else:
            return str(self._noted[y*self._w + x][0])
def main():
    game = Hitori(8, 8)
    gui_play(game)

main()
        

