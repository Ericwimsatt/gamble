from runner import Runner
from strategies import  * 

def dead_low_pair_strats():
    num_hands = 10000

    low_pair_runner = Runner("Low Dead Pair Strategies")
    low_pair_runner.add_task(("No Bet when dead pair", "Always low pair", pass_if_dead_pair, base_strategies['post_flop'], base_strategies['river'], dead_cards_matching_player_low(1), num_hands))
    low_pair_runner.add_task(("No Bet when dead pair unless both high", "Always low pair", pass_if_dead_pair_unless_ace_queen, base_strategies['post_flop'], base_strategies['river'], dead_cards_matching_player_low(1), num_hands))
    low_pair_runner.add_task(("No Bet when dead pair unless pocket pair", "Always low pair", pass_if_dead_pair_unless_pocket_pair, base_strategies['post_flop'], base_strategies['river'], dead_cards_matching_player_low(1), num_hands))
    low_pair_runner.add_task(("No Bet when dead pair unless pocket pair of eights", "Always low pair", pass_if_dead_pair_unless_eights_pocket_pair, base_strategies['post_flop'], base_strategies['river'], dead_cards_matching_player_low(1), num_hands))
    low_pair_runner.add_task(("No Bet when dead pair unless face pocket pair", "Always low pair", pass_if_dead_pair_unless_face_pocket_pair, base_strategies['post_flop'], base_strategies['river'], dead_cards_matching_player_low(1), num_hands))
    low_pair_runner.run_tasks()

def dead_high_pair_strats():
    num_hands = 10000
    high_pair_runner = Runner("High Dead Pair Strategies")
    high_pair_runner.add_task(("No Bet when dead pair", "Always high pair", pass_if_dead_pair, base_strategies['post_flop'], base_strategies['river'], dead_cards_matching_player_high(1), num_hands))
    high_pair_runner.add_task(("No Bet when dead pair unless both low", "Always high pair", pass_if_dead_pair_unless_ace_queen, base_strategies['post_flop'], base_strategies['river'], dead_cards_matching_player_high(1), num_hands))
    high_pair_runner.add_task(("No Bet when dead pair unless pocket pair", "Always high pair", pass_if_dead_pair_unless_pocket_pair, base_strategies['post_flop'], base_strategies['river'], dead_cards_matching_player_high(1), num_hands))
    high_pair_runner.add_task(("No Bet when dead pair unless pocket pair of eights", "Always high pair", pass_if_dead_pair_unless_eights_pocket_pair, base_strategies['post_flop'], base_strategies['river'], dead_cards_matching_player_high(1), num_hands))
    high_pair_runner.add_task(("No Bet when dead pair unless face pocket pair", "Always high pair", pass_if_dead_pair_unless_face_pocket_pair, base_strategies['post_flop'], base_strategies['river'], dead_cards_matching_player_high(1), num_hands))
    high_pair_runner.run_tasks()


def dead_low_pair_strats_specific():
    num_hands = 20000

    low_pair_runner = Runner("Low Dead Pair Strategies-second filter")
    low_pair_runner.add_task(("No Bet when dead pair unless both over Q", "Always low pair", pass_if_dead_pair_unless_high_cards(10), base_strategies['post_flop'], base_strategies['river'], dead_cards_matching_player_low(1), num_hands))
    low_pair_runner.add_task(("No Bet when dead pair unless both over J", "Always low pair", pass_if_dead_pair_unless_high_cards(9), base_strategies['post_flop'], base_strategies['river'], dead_cards_matching_player_low(1), num_hands))
    low_pair_runner.add_task(("No Bet when dead pair unless both over T", "Always low pair", pass_if_dead_pair_unless_high_cards(8), base_strategies['post_flop'], base_strategies['river'], dead_cards_matching_player_low(1), num_hands))
    low_pair_runner.add_task(("No Bet when dead pair unless both over 9", "Always low pair", pass_if_dead_pair_unless_high_cards(7), base_strategies['post_flop'], base_strategies['river'], dead_cards_matching_player_low(1), num_hands))
    low_pair_runner.add_task(("No Bet when dead pair unless both over 8", "Always low pair", pass_if_dead_pair_unless_high_cards(6), base_strategies['post_flop'], base_strategies['river'], dead_cards_matching_player_low(1), num_hands))
    low_pair_runner.add_task(("No Bet when dead pair unless both over 7", "Always low pair", pass_if_dead_pair_unless_high_cards(5), base_strategies['post_flop'], base_strategies['river'], dead_cards_matching_player_low(1), num_hands))

    low_pair_runner.run_tasks()

#high pair-try lower pairs
def dead_high_pair_strats_specific():
    num_hands = 20000
    high_pair_runner = Runner("High Dead Pair Strategies-second filter")
    high_pair_runner.add_task(("No Bet when dead pair unless pocket pair over 8", "Always high pair", pass_if_dead_pair_unless_min_pair_maker(6), base_strategies['post_flop'], base_strategies['river'], dead_cards_matching_player_high(1), num_hands))
    high_pair_runner.add_task(("No Bet when dead pair unless pocket pair over 7", "Always high pair", pass_if_dead_pair_unless_min_pair_maker(5), base_strategies['post_flop'], base_strategies['river'], dead_cards_matching_player_high(1), num_hands))
    high_pair_runner.add_task(("No Bet when dead pair unless pocket pair over 6", "Always high pair", pass_if_dead_pair_unless_min_pair_maker(4), base_strategies['post_flop'], base_strategies['river'], dead_cards_matching_player_high(1), num_hands))
    high_pair_runner.add_task(("No Bet when dead pair unless pocket pair over 5", "Always high pair", pass_if_dead_pair_unless_min_pair_maker(3), base_strategies['post_flop'], base_strategies['river'], dead_cards_matching_player_high(1), num_hands))
    high_pair_runner.add_task(("No Bet when dead pair unless pocket pair over 4", "Always high pair", pass_if_dead_pair_unless_min_pair_maker(2), base_strategies['post_flop'], base_strategies['river'], dead_cards_matching_player_high(1), num_hands))
    high_pair_runner.add_task(("No Bet when dead pair unless pocket pair over 3", "Always high pair", pass_if_dead_pair_unless_min_pair_maker(1), base_strategies['post_flop'], base_strategies['river'], dead_cards_matching_player_high(1), num_hands))

    high_pair_runner.run_tasks()
