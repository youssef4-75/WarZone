import neat as nt

from ai_integration.main_neat import run_neat

if __name__ == "__main__":
    config_path = "ai_integration/config.txt"
    config = nt.Config(nt.DefaultGenome, nt.DefaultReproduction, nt.DefaultSpeciesSet, nt.DefaultStagnation, config_path)
    run_neat(config)