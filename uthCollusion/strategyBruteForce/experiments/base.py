from runner import Runner
from strategies import base_strategies

def base_strat():
    runner = Runner("Base")
    runner.add_task(strategy_name="Base Strat", deads_pattern_name="None", pre_flop_strategy=base_strategies['pre_flop'], post_flop_strategy=base_strategies['post_flop'], river_strategy=base_strategies['river'], dead_card_maker=None, hands=10000)
    runner.run_tasks()

if __name__ == "__main__":
    base_strat()