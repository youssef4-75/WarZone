import os
import neat as nt

from .main_neat import run_neat

def train():
    config_path=(os.path.dirname(__file__)+'\\config.txt')
    os.chdir(os.path.dirname(__file__) + "\\neurons")
    config=nt.Config(nt.DefaultGenome, nt.DefaultReproduction,
                         nt.DefaultSpeciesSet, nt.DefaultStagnation,
                         config_path)
    run_neat(config)