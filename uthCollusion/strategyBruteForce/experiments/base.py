from runner import Runner
from strategies import base_strategies

def base_strat():
    runner = Runner("Base")
    runner.add_task(("Base Strat", "None", base_strategies['pre_flop'], base_strategies['post_flop'], base_strategies['river'], None, 10000))
    runner.run_tasks()

if __name__ == "__main__":
    base_strat()