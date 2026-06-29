from runner import Runner
from strategies import  * 
from treys import Card

def dead_low_pair_strats():
    num_hands = 10000

    low_pair_runner = Runner("Low Dead Pair Strategies")
    low_pair_runner.add_task(strategy_name="No Bet when dead pair", deads_pattern_name="Always low pair", pre_flop_strategy=pass_if_dead_pair, post_flop_strategy=base_strategies['post_flop'], river_strategy=base_strategies['river'], dead_card_maker=dead_cards_matching_player_low(1), hands=num_hands)
    low_pair_runner.add_task(strategy_name="No Bet when dead pair unless both high", deads_pattern_name="Always low pair", pre_flop_strategy=pass_if_dead_pair_unless_ace_queen, post_flop_strategy=base_strategies['post_flop'], river_strategy=base_strategies['river'], dead_card_maker=dead_cards_matching_player_low(1), hands=num_hands)
    low_pair_runner.add_task(strategy_name="No Bet when dead pair unless pocket pair", deads_pattern_name="Always low pair", pre_flop_strategy=pass_if_dead_pair_unless_pocket_pair, post_flop_strategy=base_strategies['post_flop'], river_strategy=base_strategies['river'], dead_card_maker=dead_cards_matching_player_low(1), hands=num_hands)
    low_pair_runner.add_task(strategy_name="No Bet when dead pair unless pocket pair of eights", deads_pattern_name="Always low pair", pre_flop_strategy=pass_if_dead_pair_unless_eights_pocket_pair, post_flop_strategy=base_strategies['post_flop'], river_strategy=base_strategies['river'], dead_card_maker=dead_cards_matching_player_low(1), hands=num_hands)
    low_pair_runner.add_task(strategy_name="No Bet when dead pair unless face pocket pair", deads_pattern_name="Always low pair", pre_flop_strategy=pass_if_dead_pair_unless_face_pocket_pair, post_flop_strategy=base_strategies['post_flop'], river_strategy=base_strategies['river'], dead_card_maker=dead_cards_matching_player_low(1), hands=num_hands)
    low_pair_runner.run_tasks()

def dead_high_pair_strats():
    num_hands = 10000
    high_pair_runner = Runner("High Dead Pair Strategies")
    high_pair_runner.add_task(strategy_name="No Bet when dead pair", deads_pattern_name="Always high pair", pre_flop_strategy=pass_if_dead_pair, post_flop_strategy=base_strategies['post_flop'], river_strategy=base_strategies['river'], dead_card_maker=dead_cards_matching_player_high(1), hands=num_hands)
    high_pair_runner.add_task(strategy_name="No Bet when dead pair unless both low", deads_pattern_name="Always high pair", pre_flop_strategy=pass_if_dead_pair_unless_ace_queen, post_flop_strategy=base_strategies['post_flop'], river_strategy=base_strategies['river'], dead_card_maker=dead_cards_matching_player_high(1), hands=num_hands)
    high_pair_runner.add_task(strategy_name="No Bet when dead pair unless pocket pair", deads_pattern_name="Always high pair", pre_flop_strategy=pass_if_dead_pair_unless_pocket_pair, post_flop_strategy=base_strategies['post_flop'], river_strategy=base_strategies['river'], dead_card_maker=dead_cards_matching_player_high(1), hands=num_hands)
    high_pair_runner.add_task(strategy_name="No Bet when dead pair unless pocket pair of eights", deads_pattern_name="Always high pair", pre_flop_strategy=pass_if_dead_pair_unless_eights_pocket_pair, post_flop_strategy=base_strategies['post_flop'], river_strategy=base_strategies['river'], dead_card_maker=dead_cards_matching_player_high(1), hands=num_hands)
    high_pair_runner.add_task(strategy_name="No Bet when dead pair unless face pocket pair", deads_pattern_name="Always high pair", pre_flop_strategy=pass_if_dead_pair_unless_face_pocket_pair, post_flop_strategy=base_strategies['post_flop'], river_strategy=base_strategies['river'], dead_card_maker=dead_cards_matching_player_high(1), hands=num_hands)
    high_pair_runner.run_tasks()


def dead_low_pair_strats_specific():
    num_hands = 4000

    low_pair_runner = Runner("Low Dead Pair Strategies-second filter")
    for min_rank in range(0,11):
        low_pair_runner.add_task(strategy_name="Bet Pre Flop", deads_pattern_name="Always low pair", player_hand=f"min_val {Card.STR_RANKS[min_rank]}", pre_flop_strategy=lambda _, __: True, post_flop_strategy=base_strategies['post_flop'], river_strategy=base_strategies['river'], dead_card_maker=dead_cards_matching_player_low(1), hands=num_hands, player_hand_maker=random_above_rank_inclusive(min_rank))
        low_pair_runner.add_task(strategy_name="Check Pre Flop", deads_pattern_name="Always low pair", player_hand=f"min_val {Card.STR_RANKS[min_rank]}", pre_flop_strategy=lambda _, __: False, post_flop_strategy=base_strategies['post_flop'], river_strategy=base_strategies['river'], dead_card_maker=dead_cards_matching_player_low(1), hands=num_hands, player_hand_maker=random_above_rank_inclusive(min_rank))

    low_pair_runner.run_tasks()

#high pair-try lower pairs
def dead_high_pair_strats_specific():
    num_hands = 6000
    high_pair_runner = Runner("High Dead Pair Strategies-second filter")
    for min_rank in range(0,6):
        high_pair_runner.add_task(strategy_name="Bet Pre FLop", deads_pattern_name="Always high pair", player_hand=f"Pocket {min_rank + 2}", pre_flop_strategy=lambda _, __: True, post_flop_strategy=base_strategies['post_flop'], river_strategy=base_strategies['river'], dead_card_maker=dead_cards_matching_player_high(1), hands=num_hands, player_hand_maker=pocket_pair(min_rank))
        high_pair_runner.add_task(strategy_name="Check Pre Flop", deads_pattern_name="Always high pair",  player_hand=f"Pocket {min_rank + 2}", pre_flop_strategy=lambda _, __: False, post_flop_strategy=base_strategies['post_flop'], river_strategy=base_strategies['river'], dead_card_maker=dead_cards_matching_player_high(1), hands=num_hands, player_hand_maker=pocket_pair(min_rank))

    high_pair_runner.run_tasks()
