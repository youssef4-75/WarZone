import neat 
from icecream import ic

from .training import run_simulation
from players import MachinePlayer
from core import Pin, Grid
from main import play 
from utils.var import PIN_NUMBER, GRID_SIZER, GRID_SIZEC
from .fitness import calc_fitness
from .play_to_train import playAI


def eval_genomes(genomes, config):
    f = 0
    for i, (_, genome1) in enumerate(genomes):
        n=len(genomes)
        ic(round(i/n * 100))
        genome1.fitness = 0
        for  _, genome2 in (genomes[min(i+1, n - 1):]):
            genome2.fitness = 0 if genome2.fitness == None else genome2.fitness
            f += 1
            ic(f)
            
            grid = Grid(GRID_SIZER, GRID_SIZEC)
            pl1 = MachinePlayer(0, Pin.generate_pins(PIN_NUMBER), (255, 0, 0),
                    genome1, config, grid)
            pl2 = MachinePlayer(1, Pin.generate_pins(PIN_NUMBER), (0, 255, 0),
                    genome2, config, grid)
        
            (force_quit, r_area_size, b_area_size,
                r_blunder, b_blunder, r_pins, b_pins)= playAI(pl1, pl2, grid)
            
            if force_quit:
                quit()

            calc_fitness(genome1, genome2, r_area_size, b_area_size, 
                        r_blunder, b_blunder, r_pins, b_pins)
