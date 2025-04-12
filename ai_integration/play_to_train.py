


import pygame as pg
from icecream import ic

from core import Case, Pin, Grid
from utils.var import GRID_SIZER, GRID_SIZEC, WIDTH, HEIGHT
from utils.function import draw_advanced_background

def playAI(player1, player2, grid):
    player1.set_name(0)
    player2.set_name(1)
    players = [player1, player2]
    grid.set_players(players)


    """Initialize pygame env"""
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    pg.display.set_caption("War Zone")
    surface = pg.image.load("assets/background.jpg").convert()
    clock = pg.time.Clock()


    """Start the game loop"""
    active = True
    r_blunder, b_blunder = 0, 0
    loop = 0
    while grid.get_turn() < 60 and loop<16000:
        loop += 1
        """Initial event handling"""
        for event in pg.event.get():
            if event.type == pg.QUIT:
                r_area_size, b_area_size, r_pins, b_pins = grid.analyse()
                return False, r_area_size, b_area_size, r_blunder, b_blunder, r_pins, b_pins
        
        if active:
            key, pos = players[
                grid.current_player_index()
            ].decide(grid, screen)

            
            a, b = grid.delta_move(key, pos)
            r_blunder += a
            b_blunder += b

            """Display the result"""
            draw_advanced_background(screen, surface, scale_mode="fill")
            grid.display(screen)
            grid.draw_pin(screen)
            pg.display.update()

                
        """The game end checked"""
        if grid.is_over():
            grid.display_end(screen)
            active = False
            break
    
    r_area_size, b_area_size, r_pins, b_pins = grid.analyse()
    return False, r_area_size, b_area_size, r_blunder, b_blunder, r_pins, b_pins



