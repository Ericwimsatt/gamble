from treys import Card, evaluation, Deck

#### UTILITIES ###
def eval_even_if_unfull(hand: list[int], board: list[int] = []) -> list[int]:
    ''' 
    Roughly score a hand even if it has less than 5 cards. Add the least useful cards (approximately) to get a
    sense of the value of the visible cards. 
    '''
    all_cards = hand + board
    if len(all_cards) < 5:
        extras = []
        ranks = sorted([Card.get_rank_int(card) for card in all_cards])
        # Check 1 card so we don't accidentally make a straight
        suit_barred = Card.get_suit_int(all_cards[0])
        if suit_barred == 1:
            new_suit = 2
        else:
            new_suit = 1

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

        return evaluation.evaluate(hand + extras, board)
        #Pull in dummy cards not connected to hand or board to fill out the hand for evaluation

def count_outs(player_hand: list[int], board: list[int], dead_cards: list[int] = []) -> dict[str, int]:
    '''
    Counts the number of outs for a hand given the current board and dead cards. 
    '''
    
    player_score = evaluation.evaluate(player_hand, board)

    used_cards = set(player_hand + board)

    deck = Deck()
    deck.pull_many(used_cards)
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


if __name__ == "__main__":

    print("Out count check")
    print(count_outs([Card.new('Ah'), Card.new('Kh')], [Card.new('Qh'), Card.new('Jh'), Card.new('2h')]))
    print(count_outs([Card.new('Kh'), Card.new('Ks')], [Card.new('Qh'), Card.new('Jh'), Card.new('2h')]))
    print(count_outs([Card.new('3h'), Card.new('Ks')], [Card.new('Qh'), Card.new('Jh'), Card.new('2c')]))
    print(count_outs([Card.new('Jh'), Card.new('Ks')], [Card.new('Qh'), Card.new('Jd'), Card.new('2c')]))
    print(count_outs([Card.new('Qh'), Card.new('Js')], [Card.new('Qs'), Card.new('Jh'), Card.new('2c')]))
    print(count_outs([Card.new('4h'), Card.new('Ts')], [Card.new('Qs'), Card.new('Jh'), Card.new('2c')]))






