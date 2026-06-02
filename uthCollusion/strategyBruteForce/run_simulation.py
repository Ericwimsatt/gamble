from treys import Card, Deck, evaluation

def play_game(pre_flop_strategy, post_flop_strategy, river_strategy, dead_card_maker=lambda hand: []):
    deck = Deck()
    player_hand = deck.draw(2)
    board = []
    dead_cards = deck.pull_many(dead_card_maker(player_hand))

    dealer_hand = deck.draw(2)

    player_bet = 0

    if pre_flop_strategy(player_hand, dead_cards):
        player_bet = 4

    board += deck.draw(3)
    if player_bet == 0 and  post_flop_strategy(player_hand, board, dead_cards):
        player_bet = 2

    board += deck.draw(2)
    if player_bet == 0:
        if river_strategy(player_hand, board, dead_cards):
            player_bet = 1
        else:
            return -2

    dealer_rank = evaluation.evaluate(dealer_hand, board)
    player_rank = evaluation.evaluate(player_hand, board)

    # Check if dealer qualifies
    # 2860 is max rank for a pair
    if dealer_rank > 2860:
        wager = player_bet + 2
    else:
        wager = player_bet + 1

    if player_rank < dealer_rank:
        return wager
    else:
        return -wager


def run_simulation(
    pass

if __name__ == "__main__":


    check_strategy()