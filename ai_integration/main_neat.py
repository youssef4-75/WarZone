

import neat as nt
import pickle as pk
from icecream import ic

from .evaluate import eval_genomes

from utils.var import GEN_NUMBER, WIDTH

def run_neat(config_file):
    #p = nt.Checkpointer.restore_checkpoint('neat-checkpoint-18')
    p = nt.Population(config_file)
    p.add_reporter(nt.StdOutReporter(True))
    stats = nt.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(nt.Checkpointer(1))

    winner = p.run(eval_genomes, GEN_NUMBER)
    with open("best.pickle", "wb") as f:
        pk.dump(winner, f)


