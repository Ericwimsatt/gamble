from treys import Card, evaluation, Deck
from random import random

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
        new_suit = Card.next_suit(all_cards[0])

        # if highest card is less than 5 there's a risk we make a straight, so add a 6 to prevent
        if ranks[-1] < 4:
            extras.append(Card.new_from_ints(6, new_suit))
            ranks.append(6)

        while len(all_cards) + len(extras) < 5:
            for i in range(5):
                if i not in ranks:
                    extras.append(Card.new_from_ints(i, new_suit))
                    ranks.append(i)
                    break
        hand = hand+extras

    return evaluation.evaluate(hand, board)

def count_outs(player_hand: list[int], board: list[int], dead_cards: list[int] = []) -> int:
    '''
    Counts the number of outs for a hand given the current board and dead cards. 
    '''
    
    player_score = evaluation.evaluate(player_hand, board)

    used_cards = list(player_hand + board)

    deck = Deck()
    deck.pull_many(used_cards)
    deck.pull_many(dead_cards)
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
    hand_rank = evaluation.evaluate(player_hand, board)
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

#Dead-Card Makers
def dead_cards_matching_player_high(percentage):
    def maker(player_hand):
        if random() < percentage:
            high_card = player_hand[1]
            new_card_suit = Card.next_suit(high_card)
            new_card = Card.new_from_ints(Card.get_rank_int(high_card), new_card_suit)
            while new_card == high_card or new_card == player_hand[0]:
                new_card_suit = Card.next_suit(new_card)
                new_card = Card.new_from_ints(Card.get_rank_int(high_card), new_card_suit)
            return [new_card]
    return maker

def dead_cards_matching_player_low(percentage):
    def maker(player_hand):
        if random() < percentage:
            low_card = player_hand[0]
            new_card_suit = Card.next_suit(low_card)
            new_card = Card.new_from_ints(Card.get_rank_int(low_card), new_card_suit)
            while new_card == low_card or new_card == player_hand[1]:
                new_card_suit = Card.next_suit(new_card)
                new_card = Card.new_from_ints(Card.get_rank_int(low_card), new_card_suit)

            return [new_card]
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

    print(eval_even_if_unfull([Card.new('Ah'), Card.new('As')]))
    print(eval_even_if_unfull([Card.new('Th'), Card.new('Ts')]))






