from time import time

from treys import Deck, Evaluator
from strategies import *
from gameStats import gameStats

_evaluator = Evaluator()

def _pull_many(deck, cards):
    if cards is None:
        return []
    for card in cards:
        if card in deck.cards:
            deck.cards.remove(card)
    return cards


def calc_blind_payout(player_rank):
    if player_rank <= 1: # royal flush
        return 500
    elif player_rank <= 10: # straight flush
        return 50
    elif player_rank <= 166: # four of a kind
        return 10
    elif player_rank <= 322: # full house
        return 3
    elif player_rank <= 1599: # flush
        return 1.5
    elif player_rank <= 1609: # straight
        return 1
    else:
        return 0


def play_game(pre_flop_strategy, post_flop_strategy, river_strategy, dead_card_maker, player_hand_maker=None):
    if not dead_card_maker:
        dead_card_maker = lambda hand: []
    deck = Deck()
    if player_hand_maker:
        player_hand = player_hand_maker()
        deck.pull_many(player_hand)
    else:
        player_hand = sorted(deck.draw(2))
    board = []
    dead_cards = deck.pull_many(dead_card_maker(player_hand))

    dealer_hand = deck.draw(2)

    play_bet = 0

    if pre_flop_strategy(player_hand, dead_cards):
        play_bet = 4

    board += deck.draw(3)
    if play_bet == 0 and  post_flop_strategy(player_hand, board, dead_cards):
        play_bet = 2

    board += deck.draw(2)
    if play_bet == 0:
        if river_strategy(player_hand, board, dead_cards):
            play_bet = 1

    dealer_rank = _evaluator.evaluate(dealer_hand, board)
    player_rank = _evaluator.evaluate(player_hand, board)


    round_stats = gameStats()
    round_stats.set_field('game_count', 1)
    round_stats.set_field('player_wins', 1 if player_rank < dealer_rank else 0)
    round_stats.set_field('dealer_wins', 1 if player_rank > dealer_rank else 0)
    round_stats.set_field('pushes', 1 if player_rank == dealer_rank else 0)
    round_stats.set_field('ante_bet_total', 1 if dealer_rank <= 6185 else 0)
    round_stats.set_field('dealer_qualifies', 1 if round_stats.stats['ante_bet_total'] else 0)
    round_stats.set_field('play_bet_total', play_bet)
    round_stats.set_field('player_win_play_bet_total', play_bet if round_stats.stats['player_wins'] else 0)
    round_stats.set_field('dealer_win_play_bet_total', play_bet if round_stats.stats['dealer_wins'] else 0)
    round_stats.set_field('push_play_bet_total', play_bet if round_stats.stats['pushes'] else 0)
    round_stats.set_field('blind_payout_total', calc_blind_payout(player_rank) if player_rank < dealer_rank else 0)
    round_stats.set_field('folds', 1 if play_bet == 0 else 0)
    round_stats.set_field('bad_folds', 1 if play_bet == 0 and player_rank < dealer_rank else 0)

    if round_stats.stats['folds'] == 1:
        round_stats.set_field('units_won_total', -2)
        return round_stats
    if round_stats.stats['player_wins'] == 1:
        round_stats.set_field('units_won_total', round_stats.stats['play_bet_total'] + round_stats.stats['blind_payout_total'] + round_stats.stats['ante_bet_total'])
        return round_stats
    if round_stats.stats['dealer_wins'] == 1:
        round_stats.set_field('units_won_total', -round_stats.stats['play_bet_total'] - round_stats.stats['ante_bet_total'] - 1) # blind payout
        return round_stats
    if round_stats.stats['pushes'] == 1:
        round_stats.set_field('units_won_total', 0)
        return round_stats
    else:
        raise Exception("Invalid game state: player_rank: {}, dealer_rank: {}, ".format(player_rank, dealer_rank))


def run_simulation(pre_flop_strategy, post_flop_strategy, river_strategy, dead_card_maker=None, num_hands=1000, progress_interval=30, player_hand_maker=None):
    cumulative_stats = gameStats()
    clock = time()

    for _ in range(num_hands):
        round_data = play_game(pre_flop_strategy, post_flop_strategy, river_strategy, dead_card_maker, player_hand_maker)
        cumulative_stats.accumulate(round_data)
        if time() - clock > progress_interval:
            print("Progress: {} hands played".format(_))
            clock = time()
   
    return cumulative_stats
