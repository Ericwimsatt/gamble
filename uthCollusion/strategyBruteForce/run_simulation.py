from treys import Deck, evaluation
from strategies import *

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
    def __init__(self):
        self.player_wins = 0
        self.dealer_wins = 0
        self.pushes = 0
        self.dealer_qualifies = 0
        self.play_bet_total = 0
        self.ante_bet_total = 0
        self.player_win_play_bet_total = 0
        self.dealer_win_play_bet_total = 0
        self.push_play_bet_total = 0
        self.blind_payout_total = 0
        self.folds = 0
        self.bad_folds = 0
        self.game_count = 0

    def accumulate(self, new_game_stats):
        self.player_wins += new_game_stats.player_wins
        self.dealer_wins += new_game_stats.dealer_wins
        self.pushes += new_game_stats.pushes
        self.dealer_qualifies += new_game_stats.dealer_qualifies
        self.play_bet_total += new_game_stats.play_bet_total
        self.player_win_play_bet_total += new_game_stats.player_win_play_bet_total
        self.dealer_win_play_bet_total += new_game_stats.dealer_win_play_bet_total
        self.push_play_bet_total += new_game_stats.push_play_bet_total
        self.blind_payout_total += new_game_stats.blind_payout_total
        self.folds += new_game_stats.folds
        self.bad_folds += new_game_stats.bad_folds

    def __str__(self):
        return "Player Wins: {},\n Dealer Wins: {},\n Pushes: {},\n Dealer Qualifies: {},\n Play Bet Total: {},\n Player Win Play Bet Total: {},\n Dealer Win Play Bet Total: {},\n Push Play Bet Total: {},\n Blind Payout Total: {},\n Folds: {},\n Bad Folds: {}".format(
            self.player_wins, self.dealer_wins, self.pushes, self.dealer_qualifies, self.play_bet_total, self.player_win_play_bet_total, self.dealer_win_play_bet_total, self.push_play_bet_total, self.blind_payout_total, self.folds, self.bad_folds
        )
    
    def average_str(self):
        if self.game_count == 0:
            return "No games played"
        return "Player Wins: {},\n Dealer Wins: {},\n Pushes: {},\n Dealer Qualifies: {},\n Play Bet Total: {},\n Player Win Play Bet Total: {},\n Dealer Win Play Bet Total: {},\n Push Play Bet Total: {},\n Blind Payout Total: {},\n Folds: {},\n Bad Folds: {}".format(
            self.player_wins / self.game_count, self.dealer_wins / self.game_count, self.pushes / self.game_count, self.dealer_qualifies / self.game_count, self.play_bet_total / self.game_count, self.player_win_play_bet_total / self.game_count, self.dealer_win_play_bet_total / self.game_count, self.push_play_bet_total / self.game_count, self.blind_payout_total / self.game_count, self.folds / self.game_count, self.bad_folds / self.game_count
        )

def play_game(pre_flop_strategy, post_flop_strategy, river_strategy, dead_card_maker):
    deck = Deck()
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

    dealer_rank = evaluation.evaluate(dealer_hand, board)
    player_rank = evaluation.evaluate(player_hand, board)
    ante_bet = 0

    # Check if dealer qualifies
    # 6185 is max rank for a pair
    if dealer_rank <= 6185:
        ante_bet = 1
    
    result = 0
    #fold
    if play_bet == 0:
        result = -2
    elif player_rank == dealer_rank:
        result = 0
    elif player_rank < dealer_rank:
        blind_payout = calc_blind_payout(player_rank)
        result =  play_bet + blind_payout + ante_bet
    else:
        result = - play_bet - ante_bet - 1

    round_stats = gameStats()
    round_stats.game_count = 1
    round_stats.player_wins = 1 if player_rank < dealer_rank else 0
    round_stats.dealer_wins = 1 if player_rank > dealer_rank else 0
    round_stats.pushes = 1 if player_rank == dealer_rank else 0
    round_stats.ante_bet_total = 1 if dealer_rank <= 6185 else 0
    round_stats.dealer_qualifies = 1 if ante_bet else 0
    round_stats.play_bet_total = play_bet
    round_stats.player_win_play_bet_total = play_bet if result > 0 else 0
    round_stats.dealer_win_play_bet_total = play_bet if result < 0 else 0
    round_stats.push_play_bet_total = play_bet if result == 0 else 0
    round_stats.blind_payout_total = calc_blind_payout(player_rank) if player_rank < dealer_rank else 0
    round_stats.folds = 1 if play_bet == 0 else 0
    round_stats.bad_folds = 1 if play_bet == 0 and player_rank < dealer_rank else 0

    result = 0
    if round_stats.player_wins == 1:
        result = round_stats.play_bet_total + round_stats.blind_payout_total + round_stats.ante_bet_total
        return result, round_stats
    if round_stats.dealer_wins == 1:
        result = -round_stats.play_bet_total - round_stats.ante_bet_total - 1 # blind payout
        return result, round_stats
    if round_stats.pushes == 1:
        result = 0
        return result, round_stats
    else:
        raise Exception("Invalid game state: player_rank: {}, dealer_rank: {}, result: {}".format(player_rank, dealer_rank, result))


def run_simulation(pre_flop_strategy, post_flop_strategy, river_strategy, dead_card_maker=lambda hand: [], hands=1000):
    total = 0
    cumulative_stats = gameStats()

    for _ in range(hands):
        result, round_data = play_game(pre_flop_strategy, post_flop_strategy, river_strategy, dead_card_maker)
        total += result
        cumulative_stats.accumulate(round_data)
    print("CUMULATIVE STATS:")
    print(cumulative_stats)
    print("AVERAGE STATS:")
    print(cumulative_stats.average_str())
   
    return total / hands

if __name__ == "__main__":
    #always_bet_no_deads = run_simulation(lambda hand, dead_cards: True, base_strategies['post_flop'], base_strategies['river'], hands=10000000)

    base_no_deads = run_simulation(base_strategies['pre_flop'], base_strategies['post_flop'], base_strategies['river'], hands=10000000)
    # base = run_simulation(base_strategies['pre_flop'], base_strategies['post_flop'], base_strategies['river'], 
    #                dead_card_maker=dead_cards_matching_player_high(1), hands=100000)
    # change = run_simulation(pass_if_dead_pair, base_strategies['post_flop'], base_strategies['river'], 
    #                dead_card_maker=dead_cards_matching_player_high(1), hands=100000)
    # change_ace = run_simulation(pass_if_dead_pair_unless_ace_queen, base_strategies['post_flop'], base_strategies['river'], 
    #                dead_card_maker=dead_cards_matching_player_high(1), hands =100000)
    # change_pair = run_simulation(pass_if_dead_pair_unless_pocket_pair, base_strategies['post_flop'], base_strategies['river'], 
    #                dead_card_maker=dead_cards_matching_player_high(1), hands=100000)
    # print("Base no deads: {}".format(base_no_deads))
    # print("Base-always dead card pair: {}".format(base))
    # print("Change strat -always dead card pair: {}".format(change))
    # print("Change unless ace queen -always dead card pair:: {}".format(change_ace))
    # print("Change unless pocket pair -always dead card pair:: {}".format(change_pair))