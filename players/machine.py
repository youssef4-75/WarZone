from random import randint
import neat as nt 
import pygame as pg
from icecream import ic 
from time import sleep

from .player import Player
from utils.var import PIN, MOVE, CASE, APPLY, WIDTH, HEIGHT, GRID_SIZER, GRID_SIZEC


class MachinePlayer(Player):
    def __init__(self, name, pins, color, genome, config, grid):
        super().__init__(name, pins, color)
        self.__genome = genome 
        self.__nntwork = nt.nn.FeedForwardNetwork.create(self.__genome, config)
        self.__decision = self.decide_global(grid)

    def decide_global(self, grid, rec_val=20):
        """
        Decide the next move for the machine player.
        This method should be implemented in subclasses.
        """
        DATA = []
        for line in grid.get_me():
            for case in line:
                DATA.append(1 if case.case_side is None else 0)
                DATA.append(0 if (case.case_side is None) else case.case_side)
                DATA.append(0 if case.get_pin() is None else 1)
        L = self.__nntwork.activate(DATA)
        row = L[0:8]
        column = L[8:16]
        move = L[16:18]
        pin = L[18:20]
        row = row.index(max(row))
        column = column.index(max(column))
        if move[0] > .5:
            move = "move"
        elif move[1] > .5:
            move = "invade"
        else:
            move = "revive"

        pin_selected = (pin[0]*2 + pin[1]) * 3 / 4
        pin_selected = int(pin_selected // 1)
        if pin_selected == 3: pin_selected = 0

        if rec_val == 0 or grid.validate(row, column, move, pin_selected, self.name):
            return row, column, move, int(pin_selected)
        else: return self.decide_global(grid, rec_val-1)

    def decide(self, grid, screen):
        """
        Decide the next move for the machine player.
        This method should be implemented in subclasses.
        """
        key = {
    pg.K_SPACE: 0,
    pg.K_RETURN: 0,
    pg.K_a: 0,
    pg.K_s: 0,
    pg.K_d: 0
}
        curr_phase = grid.phase()
        if curr_phase == PIN:
            if grid.pin_selected() == self.__decision[3]: 
                key[pg.K_RETURN] = randint(0, 1)
            else: 
                key[pg.K_SPACE] = randint(0, 1)
        
        elif curr_phase == MOVE:
            if self.__decision[2] == "revive":
                key[pg.K_a] = randint(0, 1)
            elif self.__decision[2] == "move":
                key[pg.K_s] = randint(0, 1)
            elif self.__decision[2] == "invade":
                key[pg.K_d] = randint(0, 1)

        elif curr_phase == CASE:
            key[pg.K_SPACE] = randint(0, 1)

        if curr_phase == APPLY:
            self.__decision = self.decide_global(grid)
            key[pg.K_RETURN] = randint(0, 1)
        

        # calculate the size of a cell
        cell_width = WIDTH / GRID_SIZER
        cell_height = HEIGHT / GRID_SIZEC
        return key, (int(self.__decision[0] * cell_width), int(self.__decision[1] * cell_height))


        