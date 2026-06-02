from treys import Card, Deck, evaluation

deck = Deck()
player_hand = deck.pull_many([Card.new('Qh'), Card.new('5d')])
deck.pull(Card.new('Ad'))

Card.print_pretty_cards(player_hand)
deck.sorted_print()

for card in player_hand:
    print(Card.get_rank_int(card), Card.get_suit_int(card), Card.int_to_pretty_str(card))

quad_3s_value = evaluation.evaluate([Card.new('3h'), Card.new('3d')], [Card.new('2s'), Card.new('8h'), Card.new('2c')])
print(quad_3s_value)

def check_strategy():
    pass

if __name__ == "__main__":


    check_strategy()