from abc import ABC, abstractmethod
from core.pin import Pin

class Player(ABC):
    """
    Abstract base class for a player in the game.
    """
    def __init__(self, name: int, pins: list[Pin], color: tuple[int]):
        self.name = name
        self.pins = pins  # List of pins owned by the player
        Pin.set_all_pins(self.pins, None, name)
        self.score = 0  # Player's score = number of cases owned
        self.color = color  # Player's color (0 or 1)
    
    def set_name(self, name: int):
        """
        Set the player's name.
        """
        self.name = name

    @abstractmethod
    def decide(self, grid, screen):
        """
        Abstract method to be implemented by subclasses to play a turn.
        """

    def __str__(self):
        return self.name
    
