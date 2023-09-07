#ESERCIZIO 7.4 HITORI, RIGHE E COLONNE

from boardgame import abstract, BoardGame, print_game, console_play
from boardgamegui1 import gui_play
import random

class Hitori(BoardGame):
    def __init__(self,w,h):
        with open ("csv_1.txt", "r") as f:
            vals = []
            for line in f:
                line_vals = line.strip("\n")
                line_vals = line_vals.split(",")
                for x in line_vals:
                    vals.append(x)
        
        self._w = w
        self._h = h

        self._board = vals
        self._black = [False]*self._w*self._h
        self._circle = [False]*self._w*self._h

        #self._solved = self._black[:]
        self._solved = ([True,False,True,False,False,False,True,False,
                         False,False,False,False,False,True,False,False,
                         True,False,False,True,False,False,False,False,
                         False,False,True,False,False,True,False,True,
                         False,True,False,True,False,False,False,False,
                         True,False,False,False,True,False,False,True,
                         False,True,False,False,False,False,False,False,
                         False,False,False,False,True,False,True,False])

        
    def cols(self):
        return self._w

    def rows(self):
        return self._h

    def black(self,x,y):
        return self._black[y * self._w + x]

    def circle(self,x,y):
        return self._circle[y * self._w + x]

    def help_1(self):
        for y in range(self._h):
            for x in range(self._w):
                if self._black[y * self._w + x] == True:
                    if y != self._h - 1:                    
                        self._circle[(y+1)*self._w + x] = True
                        self._black[(y+1)*self._w + x] = False
                    if y > 0:
                        self._circle[(y-1)*self._w + x] = True
                        self._black[(y-1)*self._w + x] = False
                    if x != self._w - 1  :
                        self._circle[y*self._w + x+1] = True
                        self._black[y*self._w + x+1] = False
                    if x > 0:
                        self._circle[y*self._w + x-1] = True
                        self._black[y*self._w + x-1] = False

    def help_2(self):
        for y in range(self._h):
            for x in range(self._w):
                value = self._board[y * self._w + x]
                if self._circle[y * self._w + x] == True:     
                    for y1 in range(self._h):
                        if self._board[y1*self._w + x] == value and (y1 != y):
                            self._black[y1*self._w + x] = True
                            self._circle[y1*self._w + x] = False
                    for x1 in range(self._w):
                        if self._board[y*self._w + x1] == value and (x1 != x):
                            self._black[y*self._w + x1] = True
                            self._circle[y*self._w + x1] = False                     
                    

        

    def finished(self):
        return self._solved == self._black

    def message(self):
        return "Puzzle solved"
        
    def play_at(self,x,y):
        self._black[y*self._w + x] = not self._black[y*self._w + x]
        self._circle[y*self._w + x] = False

        #CONTROLLO PER ANNERIRE

    def flag_at(self,x,y):
        self._circle[y*self._w + x] = not self._circle[y*self._w + x]
        self._black[y*self._w + x] = False

        #CONTROLLO PER SEGNARE

    def value_at(self,x,y):
        if self._black[y*self._w + x] == True:
            return str(self._board[y*self._w + x]) + "#"
        elif self._circle[y*self._w + x] == True:
            return str(self._board[y*self._w + x]) + "!"
        else:
            return str(self._board[y*self._w + x])
def main():
    game = Hitori(8, 8)
    gui_play(game)

main()
        
