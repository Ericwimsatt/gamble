from treys import Card, Deck, evaluation
from strategies import *

def blind_payout(player_rank):
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
    player_hand = deck.draw(2)
    board = []
    dead_cards = deck.pull_many(dead_card_maker(player_hand))

    dealer_hand = deck.draw(2)

    bet_total = 0

    if pre_flop_strategy(player_hand, dead_cards):
        bet_total = 4

    board += deck.draw(3)
    if bet_total == 0 and  post_flop_strategy(player_hand, board, dead_cards):
        bet_total = 2

    board += deck.draw(2)
    if bet_total == 0:
        if river_strategy(player_hand, board, dead_cards):
            bet_total = 1
        else:
            return -2

    dealer_rank = evaluation.evaluate(dealer_hand, board)
    player_rank = evaluation.evaluate(player_hand, board)

    # print("Evaling hand")
    # Card.print_pretty_cards(player_hand)
    # Card.print_pretty_cards(board)
    # Card.print_pretty_cards(dealer_hand)
    # evaluation.hand_summary(board, [player_hand, dealer_hand])
    if player_rank == dealer_rank:
        return 0
    
    # Check if dealer qualifies
    # 6185 is max rank for a pair
    if dealer_rank < 6185:
        bet_total = bet_total + 1

    if player_rank < dealer_rank:
        return bet_total + blind_payout(player_rank)
    else:
        return -(bet_total + 1)


def run_simulation(pre_flop_strategy, post_flop_strategy, river_strategy, dead_card_maker=lambda hand: [], hands=1000):
    total = 0
    for _ in range(hands):
        result = play_game(pre_flop_strategy, post_flop_strategy, river_strategy, dead_card_maker)
        total += result
    print("Average result: {}".format(total / hands))
    return total / hands

if __name__ == "__main__":
    base_no_deads = run_simulation(base_strategies['pre_flop'], base_strategies['post_flop'], base_strategies['river'], hands=1000000)
    base = run_simulation(base_strategies['pre_flop'], base_strategies['post_flop'], base_strategies['river'], 
                   dead_card_maker=dead_cards_matching_player_high(1), hands=100000)
    change = run_simulation(pass_if_dead_pair, base_strategies['post_flop'], base_strategies['river'], 
                   dead_card_maker=dead_cards_matching_player_high(1), hands=100000)
    change_ace = run_simulation(pass_if_dead_pair_unless_ace_queen, base_strategies['post_flop'], base_strategies['river'], 
                   dead_card_maker=dead_cards_matching_player_high(1), hands =100000)
    change_pair = run_simulation(pass_if_dead_pair_unless_pocket_pair, base_strategies['post_flop'], base_strategies['river'], 
                   dead_card_maker=dead_cards_matching_player_high(1), hands=100000)
    print("Base no deads: {}".format(base_no_deads))
    print("Base-always dead card pair: {}".format(base))
    print("Change strat -always dead card pair: {}".format(change))
    print("Change unless ace queen -always dead card pair:: {}".format(change_ace))
    print("Change unless pocket pair -always dead card pair:: {}".format(change_pair))