from treys import Card, Deck, Evaluator
from random import randint, random

_evaluator = Evaluator()

def _card_from_ints(rank_int, suit_int):
    rank_prime = Card.PRIMES[rank_int]
    bitrank = 1 << rank_int << 16
    suit = suit_int << 12
    rank = rank_int << 8
    return bitrank | suit | rank | rank_prime

def _next_suit(card):
    suits = [1, 2, 4, 8]
    suit = Card.get_suit_int(card)
    return suits[(suits.index(suit) + 1) % 4]

def _pull_many(deck, cards):
    if cards is None:
        return []
    for card in cards:
        if card in deck.cards:
            deck.cards.remove(card)
    return cards

#### UTILITIES ###
def eval_even_if_unfull(hand: list[int], board: list[int] = []) -> int:
    ''' 
    Roughly score a hand even if it has less than 5 cards. Add the least useful cards (approximately) to get a
    sense of the value of the visible cards. 
    '''
    all_cards = hand + board
    if len(all_cards) < 5:
        extras = []
        ranks = sorted([Card.get_rank_int(card) for card in all_cards])
        # Check 1 card so we don't accidentally make a straight
        new_suit = _next_suit(all_cards[0])

        # if highest card is less than 5 there's a risk we make a straight, so add a 6 to prevent
        if ranks[-1] < 4:
            extras.append(_card_from_ints(6, new_suit))
            ranks.append(6)

        while len(all_cards) + len(extras) < 5:
            for i in range(5):
                if i not in ranks:
                    extras.append(_card_from_ints(i, new_suit))
                    ranks.append(i)
                    break
        hand = hand+extras

    return _evaluator.evaluate(hand, board)

def count_outs(player_hand: list[int], board: list[int], dead_cards: list[int] = []) -> int:
    '''
    Counts the number of outs for a hand given the current board and dead cards. 
    '''
    
    player_score = _evaluator.evaluate(player_hand, board)

    used_cards = list(player_hand + board)

    deck = Deck()
    _pull_many(deck, used_cards)
    _pull_many(deck, dead_cards)
    remaining = deck.cards

    outs = []

    for card in remaining:
        dealer_score = eval_even_if_unfull([card], board)
        if dealer_score < player_score:  # lower score is better in treys
            outs.append(card)
    return len(outs)

### Default Strategy ###

def base_pre_flop(player_hand, dead_cards):
        if Card.get_rank_int(player_hand[0]) == 9 and Card.get_rank_int(player_hand[1]) >= 8:
            return True
        if Card.get_rank_int(player_hand[0]) >= 10 and Card.get_rank_int(player_hand[1]) == 6:
            return True
        if Card.get_rank_int(player_hand[0]) >= 11 and Card.get_rank_int(player_hand[1]) == 3:
            return True
        if Card.get_rank_int(player_hand[0]) >= 12:
            return True
        
def base_post_flop(player_hand, board, dead_cards):
    hand_rank = _evaluator.evaluate(player_hand, board)
    if hand_rank <= 3321: # 2 pair or better
        return True
    
    #5955 is highest pair of 3s rank
    #6185 is highest pair rank
    if hand_rank <= 5955 and eval_even_if_unfull(board) > 6185: # pair of 3s or better when there's not a pair on the board
        return True
    
    return False

def base_river(player_hand, board, dead_cards):
    if count_outs(player_hand, board, dead_cards) < 22: # if we have 2 or more outs to improve our hand, call
        return True
    return False

#optimal pre flop
#j+8
#10 + 9
# if is a pair w/ higher card, need pocket 4 or higher to bet
# If is pair w/ lower card, need A6, K8, QT to bet

#Dead-Card-Dependent
def pass_if_dead_pair(player_hand, dead_cards):
        dead_cards_ranks = [Card.get_rank_int(card) for card in dead_cards]
        if Card.get_rank_int(player_hand[0]) in dead_cards_ranks or Card.get_rank_int(player_hand[1]) in dead_cards_ranks:
            return False
        if Card.get_rank_int(player_hand[0]) == 9 and Card.get_rank_int(player_hand[1]) >= 8:
            return True
        if Card.get_rank_int(player_hand[0]) >= 10 and Card.get_rank_int(player_hand[1]) == 6:
            return True
        if Card.get_rank_int(player_hand[0]) >= 11 and Card.get_rank_int(player_hand[1]) == 3:
            return True
        if Card.get_rank_int(player_hand[0]) >= 12:
            return True
        
def pass_if_dead_pair_unless_high_cards(min_rank):
    def strategy(player_hand, dead_cards):
        if Card.get_rank_int(player_hand[0]) >= min_rank and Card.get_rank_int(player_hand[1]) >= min_rank:
            return True
        dead_cards_ranks = [Card.get_rank_int(card) for card in dead_cards]
        if Card.get_rank_int(player_hand[0]) in dead_cards_ranks or Card.get_rank_int(player_hand[1]) in dead_cards_ranks:
            return False
        if Card.get_rank_int(player_hand[0]) == 9 and Card.get_rank_int(player_hand[1]) >= 8:
            return True
        if Card.get_rank_int(player_hand[0]) >= 10 and Card.get_rank_int(player_hand[1]) == 6:
            return True
        if Card.get_rank_int(player_hand[0]) >= 11 and Card.get_rank_int(player_hand[1]) == 3:
            return True
        if Card.get_rank_int(player_hand[0]) >= 12:
            return True
    return strategy

def pass_if_dead_pair_unless_ace_queen(player_hand, dead_cards):
        if Card.get_rank_int(player_hand[0]) >= 12 and Card.get_rank_int(player_hand[1]) >= 10:
            return True
        dead_cards_ranks = [Card.get_rank_int(card) for card in dead_cards]
        if Card.get_rank_int(player_hand[0]) in dead_cards_ranks or Card.get_rank_int(player_hand[1]) in dead_cards_ranks:
            return False
        if Card.get_rank_int(player_hand[0]) == 9 and Card.get_rank_int(player_hand[1]) >= 8:
            return True
        if Card.get_rank_int(player_hand[0]) >= 10 and Card.get_rank_int(player_hand[1]) == 6:
            return True
        if Card.get_rank_int(player_hand[0]) >= 11 and Card.get_rank_int(player_hand[1]) == 3:
            return True
        

def pass_if_dead_pair_unless_pocket_pair(player_hand, dead_cards):
        hand_rank = eval_even_if_unfull(player_hand, [])
        if hand_rank <= 5955: # pair of 3s or better
            return True
        dead_cards_ranks = [Card.get_rank_int(card) for card in dead_cards]
        if Card.get_rank_int(player_hand[0]) in dead_cards_ranks or Card.get_rank_int(player_hand[1]) in dead_cards_ranks:
            return False
        if Card.get_rank_int(player_hand[0]) == 9 and Card.get_rank_int(player_hand[1]) >= 8:
            return True
        if Card.get_rank_int(player_hand[0]) >= 10 and Card.get_rank_int(player_hand[1]) == 6:
            return True
        if Card.get_rank_int(player_hand[0]) >= 11 and Card.get_rank_int(player_hand[1]) == 3:
            return True
        if Card.get_rank_int(player_hand[0]) >= 12:
            return True
def pass_if_dead_pair_unless_min_pair_maker(min_rank):
    def strategy(player_hand, dead_cards):
        if Card.get_rank_int(player_hand[0]) == Card.get_rank_int(player_hand[1]) and Card.get_rank_int(player_hand[0]) >= min_rank:
            return True
        dead_cards_ranks = [Card.get_rank_int(card) for card in dead_cards]
        if Card.get_rank_int(player_hand[0]) in dead_cards_ranks or Card.get_rank_int(player_hand[1]) in dead_cards_ranks:
            return False
        if Card.get_rank_int(player_hand[0]) == 9 and Card.get_rank_int(player_hand[1]) >= 8:
            return True
        if Card.get_rank_int(player_hand[0]) >= 10 and Card.get_rank_int(player_hand[1]) == 6:
            return True
        if Card.get_rank_int(player_hand[0]) >= 11 and Card.get_rank_int(player_hand[1]) == 3:
            return True
        if Card.get_rank_int(player_hand[0]) >= 12:
            return True
    return strategy

def pass_if_dead_pair_unless_eights_pocket_pair(player_hand, dead_cards):
        hand_rank = eval_even_if_unfull(player_hand, [])
        if hand_rank <= 4865: # pair of 8s or better
            return True
        dead_cards_ranks = [Card.get_rank_int(card) for card in dead_cards]
        if Card.get_rank_int(player_hand[0]) in dead_cards_ranks or Card.get_rank_int(player_hand[1]) in dead_cards_ranks:
            return False
        if Card.get_rank_int(player_hand[0]) == 9 and Card.get_rank_int(player_hand[1]) >= 8:
            return True
        if Card.get_rank_int(player_hand[0]) >= 10 and Card.get_rank_int(player_hand[1]) == 6:
            return True
        if Card.get_rank_int(player_hand[0]) >= 11 and Card.get_rank_int(player_hand[1]) == 3:
            return True
        if Card.get_rank_int(player_hand[0]) >= 12:
            return True

def pass_if_dead_pair_unless_face_pocket_pair(player_hand, dead_cards):
        hand_rank = eval_even_if_unfull(player_hand, [])
        if hand_rank <= 4425: # pair of 8s or better
            return True
        dead_cards_ranks = [Card.get_rank_int(card) for card in dead_cards]
        if Card.get_rank_int(player_hand[0]) in dead_cards_ranks or Card.get_rank_int(player_hand[1]) in dead_cards_ranks:
            return False
        if Card.get_rank_int(player_hand[0]) == 9 and Card.get_rank_int(player_hand[1]) >= 8:
            return True
        if Card.get_rank_int(player_hand[0]) >= 10 and Card.get_rank_int(player_hand[1]) == 6:
            return True
        if Card.get_rank_int(player_hand[0]) >= 11 and Card.get_rank_int(player_hand[1]) == 3:
            return True
        if Card.get_rank_int(player_hand[0]) >= 12:
            return True

def river_seventeen(player_hand, board, dead_cards):
    if count_outs(player_hand, board, dead_cards) < 17: 
        return True
    return False

#Dead-Card Makers
def dead_cards_matching_player_high(percentage):
    def maker(player_hand, deck):
        if random() < percentage:
            high_card = player_hand[1]
            new_card_suit = _next_suit(high_card)
            new_card = _card_from_ints(Card.get_rank_int(high_card), new_card_suit)
            while new_card == high_card or new_card == player_hand[0]:
                new_card_suit = _next_suit(new_card)
                new_card = _card_from_ints(Card.get_rank_int(high_card), new_card_suit)
            return deck.pull(new_card)
        return []
    return maker

def dead_cards_matching_player_low(percentage):
    def maker(player_hand, deck):
        if random() < percentage:
            low_card = player_hand[0]
            new_card_suit = _next_suit(low_card)
            new_card = _card_from_ints(Card.get_rank_int(low_card), new_card_suit)
            while new_card == low_card or new_card == player_hand[1]:
                new_card_suit = _next_suit(new_card)
                new_card = _card_from_ints(Card.get_rank_int(low_card), new_card_suit)
            return deck.pull(new_card)
        return []
    return maker

def draw_ten(player_hand, deck):
    return deck.draw(10)


#player_hand_maker
def pocket_pair(rank_int):
    def maker():
        suit1 = 1
        suit2 = 2
        card1 = _card_from_ints(rank_int, suit1)
        card2 = _card_from_ints(rank_int, suit2)
        return [card1, card2]
    return maker

def random_above_rank_inclusive(min_rank):
    def maker():
        hand = []
        while len(hand) < 2:
            rank_int = randint(min_rank, 12)
            suit_int = list(Card.PRETTY_SUITS.keys())[randint(0, 3)]
            card = _card_from_ints(rank_int, suit_int)
            if card not in hand:
                hand.append(card)
        return hand
    return maker

def set_both_cards(rank1, rank2):
    def maker():
        suit1 = list(Card.PRETTY_SUITS.keys())[randint(0, 3)]
        suit2 = list(Card.PRETTY_SUITS.keys())[randint(0, 3)]
        card1 = _card_from_ints(rank1, suit1)
        card2 = _card_from_ints(rank2, suit2)
        if card2 == card1:
            suit2 = _next_suit(card1)
            card2 = _card_from_ints(rank2, suit2)
        return [card1, card2]
    return maker

base_strategies = {
    'pre_flop': base_pre_flop,
    'post_flop': base_post_flop,
    'river': base_river
}

if __name__ == "__main__":

    # print("Out count check")
    # print(count_outs([Card.new('Ah'), Card.new('Kh')], [Card.new('Qh'), Card.new('Jh'), Card.new('2h')]))
    # print(count_outs([Card.new('Kh'), Card.new('Ks')], [Card.new('Qh'), Card.new('Jh'), Card.new('2h')]))
    # print(count_outs([Card.new('3h'), Card.new('Ks')], [Card.new('Qh'), Card.new('Jh'), Card.new('2c')]))
    # print(count_outs([Card.new('Jh'), Card.new('Ks')], [Card.new('Qh'), Card.new('Jd'), Card.new('2c')]))
    # print(count_outs([Card.new('Qh'), Card.new('Js')], [Card.new('Qs'), Card.new('Jh'), Card.new('2c')]))
    # print(count_outs([Card.new('4h'), Card.new('Ts')], [Card.new('Qs'), Card.new('Jh'), Card.new('2c')]))

    print(Card.get_rank_int(Card.new('Ah')), Card.get_rank_int(Card.new('Kh')), Card.get_rank_int(Card.new('Qh')), Card.get_rank_int(Card.new('Jh')), Card.get_rank_int(Card.new('Th')), Card.get_rank_int(Card.new('9h')), Card.get_rank_int(Card.new('8h')), Card.get_rank_int(Card.new('7h')), Card.get_rank_int(Card.new('6h')), Card.get_rank_int(Card.new('5h')), Card.get_rank_int(Card.new('4h')), Card.get_rank_int(Card.new('3h')), Card.get_rank_int(Card.new('2h')))



