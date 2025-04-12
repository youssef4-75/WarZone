import pygame as pg

PIN_NUMBER = 3 # Number of pins for each player
GRID_SIZER = 8 # Rows of the grid
GRID_SIZEC = 8 # Columns of the grid
KEYS = {
    pg.K_SPACE: 0,
    pg.K_RETURN: 0,
    pg.K_a: 0,
    pg.K_s: 0,
    pg.K_d: 0
}

PIN = 0
MOVE = 1
CASE = 2
APPLY = 3


WIDTH, HEIGHT = 800, 600
MARGX, MARGY = 70, 30 # Margins for the grid

CIRCLE_SIZE = 0.3

STARTX, STARTY, OUT_SIZE, SPACING = 7, 300, 30, 3

HIGHLIGHT =lambda phase: (255, 255, 0) if phase==PIN else (0, 0, 255) # Highlight color for the pin and move phase

GEN_NUMBER = 70