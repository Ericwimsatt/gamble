from treys import Card, Deck, evaluation
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

    # print("Evaling hand")
    # Card.print_pretty_cards(player_hand)
    # Card.print_pretty_cards(board)
    # Card.print_pretty_cards(dealer_hand)
    # evaluation.hand_summary(board, [player_hand, dealer_hand])

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


    return result, {
        "player_wins": 1 if result > 0 else 0,
        "dealer_wins": 1 if result < 0 else 0,
        "pushes": 1 if result == 0 else 0,
        "dealer_qualifies": 1 if ante_bet else 0,
        "play_bet_total": play_bet,
        "player_win_play_bet_total": play_bet if result > 0 else 0,
        "dealer_win_play_bet_total": play_bet if result < 0 else 0,
        "push_play_bet_total": play_bet if result == 0 else 0,
        "blind_payout_total": blind_payout if result > 0 else 0,
        "folds": 1 if play_bet == 0 else 0,
        "bad_folds": 1 if play_bet == 0 and player_rank < dealer_rank else 0
    }

def run_simulation(pre_flop_strategy, post_flop_strategy, river_strategy, dead_card_maker=lambda hand: [], hands=1000):
    total = 0
    play_stats = {
        "player_wins": 0,
        "dealer_wins": 0,
        "pushes": 0,
        "dealer_qualifies": 0,
        "play_bet_total": 0,
        "player_win_play_bet_total": 0,
        "dealer_win_play_bet_total": 0,
        "push_play_bet_total": 0,
        "blind_payout_total": 0,
        "folds": 0,
        "bad_folds": 0
    }
    for _ in range(hands):
        result, round_data = play_game(pre_flop_strategy, post_flop_strategy, river_strategy, dead_card_maker)
        total += result
        for key in play_stats:
            play_stats[key] += round_data.get(key, 0)
    print("Average result: {}".format(total / hands))
    for key in play_stats:
        print("TOTAL {} : {}".format(key, play_stats[key]))
    print("________")
    for key in play_stats:
        print("AVERAGE {} : {}".format(key, play_stats[key] / hands))
    return total / hands

if __name__ == "__main__":
    always_bet_no_deads = run_simulation(lambda hand, dead_cards: True, base_strategies['post_flop'], base_strategies['river'], hands=10000000)

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