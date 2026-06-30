from runner import Runner
from strategies import *
from treys import Card


def river_using_dead_cards():
    num_hands = 50000
    runner = Runner("River Using Dead Cards")
    runner.add_task(strategy_name="river 17 outs", deads_pattern_name="10 random", pre_flop_strategy=base_strategies['pre_flop'], post_flop_strategy=base_strategies['post_flop'], river_strategy=river_seventeen, dead_card_maker=draw_ten, hands=num_hands)
    runner.add_task(strategy_name="river 22 outs", deads_pattern_name="10 random", pre_flop_strategy=base_strategies['pre_flop'], post_flop_strategy=base_strategies['post_flop'], river_strategy=base_strategies['river'], dead_card_maker=draw_ten, hands=num_hands)
    runner.add_task(strategy_name="river 22 outs", pre_flop_strategy=base_strategies['pre_flop'], post_flop_strategy=base_strategies['post_flop'], river_strategy=base_strategies['river'], hands=num_hands)

    runner.run_tasks()