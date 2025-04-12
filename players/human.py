from .player import Player
import pygame as pg
from icecream import ic 
from time import sleep


class HumanPlayer(Player):
    """
    Class representing a human player in the game.
    """
    def __init__(self, name: str, pins: list, color: tuple[int]):
        super().__init__(name, pins, color)

    def decide(self, grid, screen):
        return pg.key.get_pressed(), pg.mouse.get_pos()
    
    def __str__(self):
        return f"Human Player: {self.name}"