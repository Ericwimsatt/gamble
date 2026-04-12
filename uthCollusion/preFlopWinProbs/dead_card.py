from typing import List, Optional

from uthCollusion.preFlopWinProbs.uthSimulation import checkOdds


RANKS = ['A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2']
SUITS = ['c', 'd', 'h', 's']


def find_lowest_winning_hand(start_high_card='J', start_low_card='9', num_higher_cards=None, num_simulations=5000, dead_cards_fn=None):
    """
    Find the lowest hand that still has >50% win rate.
    """
    ranks = RANKS
    suits = ['h', 'c']
    
    high_idx = ranks.index(start_high_card)
    
    hands_to_test = []
    
    for i in range(high_idx, len(ranks)):
        for j in range(i + 1, len(ranks)):
            hand = [ranks[i] + suits[0], ranks[j] + suits[1]]
            hands_to_test.append(hand)
    
    hands_tested = []
    lowest_winning_hand = None
    lowest_winning_rate = 0
    found_losing_hand = False
    
    for hand in hands_to_test:
        if dead_cards_fn is not None:
            result = checkOdds(hand, dead_cards_fn, simulations=num_simulations)
        elif num_higher_cards is not None:
            hand_generator = create_unified_dead_cards_fn(over_cards=num_higher_cards, playerHand=hand)
            if hand_generator is None:
                continue
            result = checkOdds(hand, hand_generator, simulations=num_simulations)
        else:
            result = checkOdds(hand, None, simulations=num_simulations)
        
        final_win_rate = result['win_rate']
        total_sims = result['total_simulations']
        
        is_winning = final_win_rate > 0.50
        
        hand_result = {
            'hand': hand,
            'win_rate': final_win_rate,
            'total_simulations': total_sims,
            'is_winning': is_winning
        }
        hands_tested.append(hand_result)
        
        if is_winning:
            lowest_winning_hand = hand
            lowest_winning_rate = final_win_rate
        else:
            found_losing_hand = True
        
        if found_losing_hand or hand[1].startswith('2'):
            break
    
    return {
        'lowest_winning_hand': lowest_winning_hand,
        'lowest_winning_rate': lowest_winning_rate,
        'hands_tested': hands_tested,
        'total_hands_tested': len(hands_tested),
        'start_cards': [start_high_card, start_low_card],
        'num_higher_cards': num_higher_cards
    }


def generate_dead_cards_unified(
    num_dead_cards: int = 10,
    over_cards: int = 3,
    playerHand: List[str] = [],
    suit_match_count: int = 0,
    upper_pair_count: int = 0,
    lower_pair_count: int = 0
) -> Optional[List[str]]:
    import random
    
    if len(playerHand) not in (0, 2):
        raise ValueError("playerHand must have 0 or 2 cards")
    
    if upper_pair_count > 3:
        raise ValueError("upper_pair_count cannot be greater than 3 (there are 4 cards of each value in the deck)")
    
    ranks = RANKS
    suits = SUITS
    
    full_deck = [r + s for r in ranks for s in suits]
    
    if len(playerHand) == 0:
        random.shuffle(full_deck)
        return full_deck[:min(num_dead_cards, len(full_deck))]
    
    player_ranks = [card[0] for card in playerHand]
    high_rank = min(player_ranks, key=lambda r: ranks.index(r))
    low_rank = max(player_ranks, key=lambda r: ranks.index(r))
    high_idx = ranks.index(high_rank)
    low_idx = ranks.index(low_rank)
    
    high_suit = min(playerHand, key=lambda c: ranks.index(c[0]))[1]
    
    for card in playerHand:
        if card in full_deck:
            full_deck.remove(card)
    
    random.shuffle(full_deck)
    
    dead_cards = []
    remaining_deck = list(full_deck)
    
    if upper_pair_count > 0:
        cards_added = 0
        for card in list(remaining_deck):
            if card[0] == high_rank and cards_added < upper_pair_count:
                dead_cards.append(card)
                remaining_deck.remove(card)
                cards_added += 1
        if cards_added < upper_pair_count:
            return None
    
    if lower_pair_count > 0:
        cards_added = 0
        for card in list(remaining_deck):
            if card[0] == low_rank and cards_added < lower_pair_count:
                dead_cards.append(card)
                remaining_deck.remove(card)
                cards_added += 1
        if cards_added < lower_pair_count:
            return None
    
    remaining_over_cards = over_cards
    
    if suit_match_count > 0:
        cards_added = 0
        player_rank_set = set(player_ranks)
        for card in list(remaining_deck):
            if card[1] == high_suit and card[0] not in player_rank_set:
                card_rank_idx = ranks.index(card[0])
                if card_rank_idx < high_idx:
                    if remaining_over_cards > 1:
                        dead_cards.append(card)
                        remaining_deck.remove(card)
                        remaining_over_cards -= 1
                        cards_added += 1
                        if cards_added >= suit_match_count:
                            break
                    else:
                        pass
                else:
                    dead_cards.append(card)
                    remaining_deck.remove(card)
                    cards_added += 1
                    if cards_added >= suit_match_count:
                        break
        if cards_added < suit_match_count:
            return None
    
    if remaining_over_cards > 0:
        cards_added = 0
        player_rank_set = set(player_ranks)
        for card in list(remaining_deck):
            if ranks.index(card[0]) < high_idx and card[0] not in player_rank_set and card[1] != high_suit:
                dead_cards.append(card)
                remaining_deck.remove(card)
                cards_added += 1
                if cards_added >= remaining_over_cards:
                    break
        if cards_added < remaining_over_cards:
            return None
    
    remaining_needed = num_dead_cards - len(dead_cards)
    if remaining_needed > 0:
        cards_added = 0
        player_rank_set = set(player_ranks)
        for card in list(remaining_deck):
            if ranks.index(card[0]) > high_idx and card[0] not in player_rank_set:
                dead_cards.append(card)
                remaining_deck.remove(card)
                cards_added += 1
                if cards_added >= remaining_needed:
                    break
    
    random.shuffle(dead_cards)
    return dead_cards[:num_dead_cards]


class UnifiedDeadCardsGenerator:
    def __init__(
        self,
        num_dead_cards: int = 10,
        over_cards: int = 3,
        playerHand: List[str] = [],
        suit_match_count: int = 0,
        upper_pair_count: int = 0,
        lower_pair_count: int = 0
    ):
        self.num_dead_cards = num_dead_cards
        self.over_cards = over_cards
        self.playerHand = playerHand
        self.suit_match_count = suit_match_count
        self.upper_pair_count = upper_pair_count
        self.lower_pair_count = lower_pair_count
    
    def __call__(self) -> Optional[List[str]]:
        return generate_dead_cards_unified(
            num_dead_cards=self.num_dead_cards,
            over_cards=self.over_cards,
            playerHand=self.playerHand,
            suit_match_count=self.suit_match_count,
            upper_pair_count=self.upper_pair_count,
            lower_pair_count=self.lower_pair_count
        )


def create_unified_dead_cards_fn(
    num_dead_cards: int = 10,
    over_cards: int = 3,
    playerHand: List[str] = [],
    suit_match_count: int = 0,
    upper_pair_count: int = 0,
    lower_pair_count: int = 0
):
    if len(playerHand) == 2:
        ranks = RANKS
        suits = SUITS
        player_ranks = [card[0] for card in playerHand]
        high_rank = min(player_ranks, key=lambda r: ranks.index(r))
        low_rank = max(player_ranks, key=lambda r: ranks.index(r))
        high_idx = ranks.index(high_rank)

        over_cards_pool = []
        for i in range(high_idx):
            for suit in suits:
                card = ranks[i] + suit
                if card not in playerHand:
                    over_cards_pool.append(card)

        if over_cards > len(over_cards_pool):
            return None

        required_cards = over_cards + upper_pair_count + lower_pair_count
        if required_cards > num_dead_cards:
            return None

    return UnifiedDeadCardsGenerator(
        num_dead_cards=num_dead_cards,
        over_cards=over_cards,
        playerHand=playerHand,
        suit_match_count=suit_match_count,
        upper_pair_count=upper_pair_count,
        lower_pair_count=lower_pair_count
    )
