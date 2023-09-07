import g2d
from boardgame import BoardGame
from time import time
from Hitori import black, circle

W, H = 40, 40
LONG_PRESS = 0.5

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
        elif g2d.key_pressed("Spacebar"):
            self._game.help_1()
        elif g2d.key_pressed("Enter"):
            self._game.help_2()
        self.update_buttons()

    def update_buttons(self):
        g2d.clear_canvas()
        g2d.set_color((0, 0, 0))
        cols, rows = self._game.cols(), self._game.rows()
        for y in range(1, rows):
            g2d.draw_line((0, y * H), (cols * W, y * H))
        for x in range(1, cols):
            g2d.draw_line((x * W, 0), (x * W, rows * H))
        for y in range(rows):
            for x in range(cols):
                value = self._game.value_at(x, y)
                center = x * W + W//2, y * H + H//2
                c1 = x * W + W//2, y * H + H//2,w,h
                if Hitori.black(x,y):
                    g2d.set_color((0,0,0))
                    g2d.fill_rect(c)
                    g2d.set_color((255,255,255))
                    g2d.draw_text_centered(value, center, H//2)
                elif Hitori.circle(x,y):
                    g2d.set_color((255,255,153))
                    g2d.fill_rect(c)
                    g2d.set_color((0,0,0))
                    g2d.draw_text_centered(value, center, H//2)
                else:
                    g2d.set_color((255,255,255))
                    g2d.fill_rect(c)
                    g2d.set_color((0,0,0))
                    g2d.draw_text_centered(value, center, H//2)
                    
        g2d.update_canvas()
        if self._game.finished():
            g2d.alert(self._game.message())
            g2d.close_canvas()

def gui_play(game: BoardGame):
    g2d.init_canvas((game.cols() * W, game.rows() * H))
    ui = BoardGameGui(game)
    g2d.main_loop(ui.tick)

