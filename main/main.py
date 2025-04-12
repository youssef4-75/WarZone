from core import Case, Pin, Grid
import pygame as pg
from utils.var import GRID_SIZER, GRID_SIZEC, WIDTH, HEIGHT
from utils.function import draw_advanced_background

def play(player1, player2):
    grid = Grid(GRID_SIZER, GRID_SIZEC)
    player1.set_name(0)
    player2.set_name(1)
    players = [player1, player2]
    grid.set_players(players)


    """Initialize pygame env"""
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    pg.display.set_caption("War Zone")
    surface = pg.image.load("assets/background.jpg").convert()
    clock = pg.time.Clock()
    running = True


    """Start the game loop"""
    active = True
    while running:
        """Initial event handling"""
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
        
        if active:
            key, pos = players[
                grid.current_player_index()
            ].decide(grid, screen)

            grid.delta_move(key, pos)

            """Display the result"""
            draw_advanced_background(screen, surface, scale_mode="fill")
            grid.display(screen)
            grid.draw_pin(screen)
            pg.display.update()
            clock.tick(60)

                
        """The game end checked"""
        if grid.is_over():
            grid.display_end(screen)
            active = False
            break




