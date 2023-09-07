import g2d
from time import time
import random

W, H = 40, 40
LONG_PRESS = 0.5

def abstract():
    raise NotImplementedError("Abstract method")

class BoardGame:
    def play_at(self, x: int, y: int): abstract()
    def flag_at(self, x: int, y: int): abstract()
    def value_at(self, x: int, y: int) -> str: abstract()
    def help_1(self): abstract()
    def help_2(self): abstract()
    def cols(self) -> int: abstract()
    def rows(self) -> int: abstract()
    def finished(self) -> bool: abstract()
    def message(self) -> str: abstract()

def print_game(game: BoardGame):
    for y in range(game.rows()):
        for x in range(game.cols()):
            val = game.value_at(x, y)
            print(f"{val:3}", end='')
        print()

def console_play(game: BoardGame):
    print_game(game)

    while not game.finished():
        x, y = input().split()
        game.play_at(int(x), int(y))
        print_game(game)

    print(game.message())

class BoardGameGui:
    def __init__(self, g: BoardGame):
        self._game = g
        self._downtime = 0
        self.update_buttons()

    def tick(self):
        if g2d.key_pressed("LeftButton"):
            self._downtime = time()
        elif g2d.key_released("LeftButton"):
            mouse = g2d.mouse_position()
            x, y = mouse[0] // W, mouse[1] // H
            if time() - self._downtime > LONG_PRESS:
                self._game.flag_at(x, y)
            else:
                self._game.play_at(x, y)
                
        elif g2d.key_pressed("Spacebar"): #Aiuto 1: cerchia le celle adiacenti alle celle annerite
            self._game.auto_1()
        elif g2d.key_pressed("Enter"): #Aiuto 2: annerisce le celle sulla stessa riga/colonna con lo stesso valore delle celle cerchiate
            self._game.auto_2()
            
        self.update_buttons()
        
        self._game.rule_1() #Controlla le regole ogni chiamata di tick
        self._game.rule_2()
        self._game.rule_3()


    def update_buttons(self):
        g2d.clear_canvas()
        cols, rows = self._game.cols(), self._game.rows()
            
        for y in range(rows):
            for x in range(cols):
                value = self._game.value_at(x, y)
                center = x * W + W//2, y * H + H//2
                c = x * W , y * H ,W,H
                if self._game.black(x,y): #In nero le celle annerite
                    g2d.set_color((0,0,0))
                    g2d.fill_rect(c)
                    g2d.set_color((255,255,255))
                    g2d.draw_text_centered(value, center, H//2)
                elif self._game.circle(x,y): #In giallo le celle cerchiate
                    g2d.set_color((255,255,153))
                    g2d.fill_rect(c)
                    g2d.set_color((0,0,0))
                    g2d.draw_text_centered(value, center, H//2)
                else:
                    g2d.set_color((0,0,0))
                    g2d.draw_text_centered(value, center, H//2)

        for y in range(1, rows):
            g2d.set_color((0, 0, 0))
            g2d.draw_line((0, y * H), (cols * W, y * H))
            
        for x in range(1, cols):
            g2d.set_color((0, 0, 0))
            g2d.draw_line((x * W, 0), (x * W, rows * H))
        
                    
        g2d.update_canvas()
        if self._game.finished():
            g2d.alert(self._game.message())
            g2d.close_canvas()

def gui_play(game: BoardGame):
    g2d.init_canvas((game.cols() * W, game.rows() * H))
    ui = BoardGameGui(game)
    g2d.main_loop(ui.tick)



class Hitori(BoardGame):
    def __init__(self,w,h):
        with open ("test_1.txt", "r") as f:
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
        self._rule_3 = [False]*self._w*self._h

        
    def cols(self):
        return self._w

    def rows(self):
        return self._h

    def rule_1(self): #Celle nere non adiacienti
        condition = []
        for y in range(self._h):
            for x in range(self._w):
                if self._black[y * self._w + x] == True and y != self._h - 1 and self._black[(y+1)*self._w + x] == True:
                    condition.append(True)
                if self._black[y * self._w + x] == True and y > 0 and self._black[(y-1)*self._w + x] == True:
                    condition.append(True)
                if  self._black[y * self._w + x] == True and x != self._w - 1 and self._black[y*self._w + x+1] == True:
                    condition.append(True)
                if self._black[y * self._w + x] == True and x > 0 and self._black[y*self._w + x - 1] == True:
                    condition.append(True)
                else:
                    pass

        return any(condition)

    def rule_2(self): # Celle non annerite non molteplici per riga e colonna
        condition = []
        for y in range(self._h):
            for x in range(self._w):
                value = self._board[y * self._w + x]
                if self._black[y * self._w + x] == False:     
                    for y1 in range(self._h):
                        if  self._black[y1*self._w + x] == False and self._board[y1*self._w + x] == value and (y1 != y):
                            condition.append(True) #La regola è violata

                    for x1 in range(self._w):
                        if self._black[y*self._w + x1] == False and self._board[y*self._w + x1] == value and (x1 != x):
                            condition.append(True) #La regola è violata

        return any(condition)



    def rule_3(self):
        self._rule_3 = [False]*self._w*self._h #A ogni chiamata della regola, azzero la matrice dei bianchi e ricomincio a contare
        r = 0
        b = 0
        for y in range(self._h):
            for x in range(self._w): 
                if self._black[y * self._w + x] == False:
                    self.control_3(x,y)
                    
        for element in self._rule_3:
            if element == True:
                r+=1
        for el1 in self._black:
            if el1 == False:
                b+=1
    
        if r != b: #Confronto le celle bianche teoricamente adiacenti con le cellule bianche effettive
            return True #La regola è violata
        else:
            return False


    
    def control_3(self,x,y): #Celle non annerite adiacenti fra loro (con ricorsione)             
        self._rule_3[y * self._w + x] == True
        if y != self._h - 1 and self._black[(y+1)*self._w + x] == False and self._rule_3[(y+1)*self._w + x] != True :
            self._rule_3[(y+1)*self._w + x] = True
            self.control_3(x,y+1)
        if y > 0 and self._black[(y-1)*self._w + x] == False and self._rule_3[(y-1)*self._w + x] != True:
            self._rule_3[(y-1)*self._w + x] = True
            self.control_3(x,y-1)
        if x != self._w - 1 and self._black[y*self._w + x+1] == False and self._rule_3[y*self._w + x+1] != True:
            self._rule_3[y*self._w + x+1] = True
            self.control_3(x+1,y)
        if x > 0 and self._black[y*self._w + x - 1] == False and self._rule_3[y*self._w + x-1] != True:
            self._rule_3[y*self._w + x-1] = True
            self.control_3(x-1,y)
        else:
            pass
        

    def black(self,x,y):
        return self._black[y * self._w + x]

    def circle(self,x,y):
        return self._circle[y * self._w + x]

    def auto_1(self): #Aiuto 1: cerchia le celle adiacenti alle celle annerite (se queste non sono già annerite)
        for y in range(self._h):
            for x in range(self._w):
                if self._black[y * self._w + x] == True:
                    if y != self._h - 1 and self._black[(y+1)*self._w + x] == False:                    
                        self._circle[(y+1)*self._w + x] = True
                    if y > 0 and self._black[(y-1)*self._w + x] == False:
                        self._circle[(y-1)*self._w + x] = True                     
                    if x != self._w - 1 and self._black[y*self._w + x+1] == False:
                        self._circle[y*self._w + x+1] = True
                    if x > 0 and self._black[y*self._w + x-1] == False:
                        self._circle[y*self._w + x-1] = True

    def auto_2(self): #Aiuto 2: annerisce le celle sulla stessa riga/colonna con lo stesso valore delle celle cerchiate (se questa non è già cerchiata)
        for y in range(self._h):
            for x in range(self._w):
                value = self._board[y * self._w + x]
                if self._circle[y * self._w + x] == True:     
                    for y1 in range(self._h):
                        if self._board[y1*self._w + x] == value and (y1 != y) and self._circle[y1*self._w + x] == False:
                            self._black[y1*self._w + x] = True

                    for x1 in range(self._w):
                        if self._board[y*self._w + x1] == value and (x1 != x) and self._circle[y*self._w + x1] == False:
                            self._black[y*self._w + x1] = True
                            


    def wrong(self):
        if self.rule_1() == True or self.rule_2() == True or self.rule_3() == True:
            return True
        else:
            return False

    def finished(self): #Tutte le regole non devono essere violate
        if self.rule_1() == False and self.rule_2() == False and self.rule_3() == False:
            return True
        

    def message(self):
        return "Puzzle solved"
        
    def play_at(self,x,y): #Comando per annerire
        self._black[y*self._w + x] = not self._black[y*self._w + x]
        self._circle[y*self._w + x] = False

    def flag_at(self,x,y): #Comando per cerchiare
        self._circle[y*self._w + x] = not self._circle[y*self._w + x]
        self._black[y*self._w + x] = False

    def value_at(self,x,y):
        return str(self._board[y*self._w + x])

    
def main():
    game = Hitori(9, 9)
    gui_play(game)

main()
        
