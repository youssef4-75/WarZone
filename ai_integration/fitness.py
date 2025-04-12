

def calc_fitness(genome1, genome2, 
                red_area_size: int, blue_area_size: int, 
                red_blunder: int, blue_blunder: int,
                red_pins: int, blue_pins: int):
    """logic to calculate the fitness of each genome"""
    genome1.fitness += red_area_size - red_blunder + (red_pins * 2)
    genome2.fitness += blue_area_size - blue_blunder + (blue_pins * 2)
