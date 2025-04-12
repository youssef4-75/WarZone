from main import play
from core import Pin 
from players import HumanPlayer
from utils.var import PIN_NUMBER

if __name__ == "__main__":
    pl1 = HumanPlayer(0, Pin.generate_pins(PIN_NUMBER), (255, 0, 0))
    pl2 = HumanPlayer(1, Pin.generate_pins(PIN_NUMBER), (0, 255, 0))
    play(pl1, pl2)