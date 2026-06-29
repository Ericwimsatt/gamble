from time import time

from treys import Deck, Evaluator
from strategies import *

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

class gameStats:
    stats = {}
    def __init__(self):
        self.stats ={
            'units_won_total': 0,
            'player_wins': 0,
            'dealer_wins': 0,
            'pushes': 0,
            'dealer_qualifies': 0,
            'play_bet_total': 0,
            'ante_bet_total': 0,
            'player_win_play_bet_total': 0,
            'dealer_win_play_bet_total': 0,
            'push_play_bet_total': 0,
            'blind_payout_total': 0,
            'folds': 0,
            'bad_folds': 0,
            'game_count': 0
        }

    def accumulate(self, new_game_stats):
        for key in self.stats.keys():
            self.stats[key] += new_game_stats.stats[key]

    def set_field(self, field, value):
        self.stats[field] = value
    
    def average_units_won(self):
        if self.stats['game_count'] == 0:
            return 0
        return self.stats['units_won_total'] / self.stats['game_count']
        
    def __str__(self):
        out_str = "Game Stats:\n"
        for key in self.stats.keys():
            out_str += "{}: {}\n".format(key, self.stats[key])
        return out_str

    
    def average_str(self):
        if self.stats['game_count'] == 0:
            return "No games played"
        out_str = "Average Game Stats:\n"
        for key in self.stats.keys():
            out_str += "{}: {}\n".format(key, self.stats[key] / self.stats['game_count'])
        return out_str

def play_game(pre_flop_strategy, post_flop_strategy, river_strategy, dead_card_maker):
    if not dead_card_maker:
        dead_card_maker = lambda hand: []
    deck = Deck()
    player_hand = sorted(deck.draw(2))
    board = []
    dead_cards = _pull_many(deck, dead_card_maker(player_hand))

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


def run_simulation(pre_flop_strategy, post_flop_strategy, river_strategy, dead_card_maker=lambda hand: [], hands=1000, progress_interval=30):
    cumulative_stats = gameStats()
    clock = time()

    for _ in range(hands):
        round_data = play_game(pre_flop_strategy, post_flop_strategy, river_strategy, dead_card_maker)
        cumulative_stats.accumulate(round_data)
        if time() - clock > progress_interval:
            print("Progress: {} hands played".format(_))
            clock = time()
   
    return cumulative_stats

if __name__ == "__main__":
    base_no_deads = run_simulation(base_strategies['pre_flop'], base_strategies['post_flop'], base_strategies['river'], hands=100000)
    print("Skip low dead pair always")
    skip_low_dead_pair = run_simulation(pass_if_dead_pair, base_strategies['post_flop'], base_strategies['river'], dead_cards_matching_player_low(1), hands=10000)
    print("Except AQ")
    skip_low_dead_pair_except_AQ = run_simulation(pass_if_dead_pair_unless_ace_queen, base_strategies['post_flop'], base_strategies['river'], dead_cards_matching_player_low(1), hands=10000)
    print("Except pair 3s")
    skip_low_dead_pair_except_pocket = run_simulation(pass_if_dead_pair_unless_pocket_pair, base_strategies['post_flop'], base_strategies['river'], dead_cards_matching_player_low(1), hands=10000)
    print("Except pair  eights")
    skip_low_dead_pair_except_eights = run_simulation(pass_if_dead_pair_unless_eights_pocket_pair, base_strategies['post_flop'], base_strategies['river'], dead_cards_matching_player_low(1), hands=10000)
    print("except pair  face")
    skip_low_dead_pair_except_face = run_simulation(pass_if_dead_pair_unless_face_pocket_pair, base_strategies['post_flop'], base_strategies['river'], dead_cards_matching_player_low(1), hands=10000)
