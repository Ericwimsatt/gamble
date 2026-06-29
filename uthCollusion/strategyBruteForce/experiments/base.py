from runner import Runner
from strategies import *
from treys import Card

def base_strat():
    runner = Runner("Base")
    runner.add_task(strategy_name="Base Strat", deads_pattern_name="None", pre_flop_strategy=base_strategies['pre_flop'], post_flop_strategy=base_strategies['post_flop'], river_strategy=base_strategies['river'], dead_card_maker=None, hands=10000)
    runner.run_tasks()

def base_check():
    num_hands = 2000
    runner = Runner("Base Strat Check")
    for high_rank in range(7,10):
        for low_rank in range(0, high_rank):
            runner.add_task(strategy_name="Bet Pre Flop", deads_pattern_name=f"No Known Dead", player_hand=f"{Card.STR_RANKS[high_rank]} + {Card.STR_RANKS[low_rank]} ", pre_flop_strategy=lambda _, __: True, post_flop_strategy=base_strategies['post_flop'], river_strategy=base_strategies['river'], hands=num_hands, player_hand_maker=set_both_cards(high_rank, low_rank))
            runner.add_task(strategy_name="Check Pre Flop", deads_pattern_name=f"No Known Dead", player_hand=f"{Card.STR_RANKS[high_rank]} + {Card.STR_RANKS[low_rank]} ", pre_flop_strategy=lambda _, __: False, post_flop_strategy=base_strategies['post_flop'], river_strategy=base_strategies['river'], hands=num_hands, player_hand_maker=set_both_cards(high_rank, low_rank))
    runner.run_tasks()

if __name__ == "__main__":
    base_check()