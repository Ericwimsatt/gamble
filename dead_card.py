from typing import List, Optional

from uthSimulation import checkOdds


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
    
    if len(playerHand) == 0:
        all_cards = [r + s for r in ranks for s in suits]
        return random.sample(all_cards, min(num_dead_cards, len(all_cards)))
    
    player_ranks = [card[0] for card in playerHand]
    high_rank = max(player_ranks, key=lambda r: ranks.index(r))
    low_rank = min(player_ranks, key=lambda r: ranks.index(r))
    high_idx = ranks.index(high_rank)
    
    first_card_suit = playerHand[0][1]
    
    upper_pair_cards = []
    for suit in suits:
        card = high_rank + suit
        if card not in playerHand:
            upper_pair_cards.append(card)
    if upper_pair_count > len(upper_pair_cards):
        return None
    
    lower_pair_cards = []
    for suit in suits:
        card = low_rank + suit
        if card not in playerHand:
            lower_pair_cards.append(card)
    if lower_pair_count > len(lower_pair_cards):
        return None
    
    suit_match_cards = []
    for r in ranks:
        for s in suits:
            if s == first_card_suit:
                card = r + s
                if card not in playerHand:
                    suit_match_cards.append(card)
    available_suit_match = [c for c in suit_match_cards if c not in upper_pair_cards[:upper_pair_count] and c not in lower_pair_cards[:lower_pair_count]]
    if suit_match_count > len(available_suit_match):
        return None
    
    over_cards_pool = []
    for i in range(high_idx):
        for suit in suits:
            card = ranks[i] + suit
            if card not in playerHand:
                over_cards_pool.append(card)
    
    if over_cards > len(over_cards_pool):
        return None
    
    dead_cards = []
    
    lower_cards_pool = []
    for i in range(high_idx + 1, len(ranks)):
        for suit in suits:
            card = ranks[i] + suit
            if card not in playerHand and ranks[i] != low_rank:
                lower_cards_pool.append(card)
    
    reserved_cards = set()
    
    if upper_pair_count > 0:
        selected_upper_pairs = random.sample(upper_pair_cards, upper_pair_count)
        dead_cards.extend(selected_upper_pairs)
        reserved_cards.update(selected_upper_pairs)
    
    if lower_pair_count > 0:
        available_lower_pairs = [c for c in lower_pair_cards if c not in reserved_cards]
        selected_lower_pairs = random.sample(available_lower_pairs, min(lower_pair_count, len(available_lower_pairs)))
        dead_cards.extend(selected_lower_pairs)
        reserved_cards.update(selected_lower_pairs)
    
    remaining_dead_cards = num_dead_cards - len(dead_cards)
    
    suited_cards_needed = suit_match_count
    over_cards_needed = over_cards
    
    cards_that_are_both_suited_and_over = []
    for r in ranks[:high_idx]:
        for s in suits:
            if s == first_card_suit:
                card = r + s
                if card not in playerHand and card not in reserved_cards:
                    cards_that_are_both_suited_and_over.append(card)
    
    if suited_cards_needed + over_cards_needed > remaining_dead_cards:
        overlap_needed = suited_cards_needed + over_cards_needed - remaining_dead_cards
        if overlap_needed > len(cards_that_are_both_suited_and_over):
            return None
        selected_overlap = random.sample(cards_that_are_both_suited_and_over, overlap_needed)
        dead_cards.extend(selected_overlap)
        reserved_cards.update(selected_overlap)
        remaining_dead_cards = num_dead_cards - len(dead_cards)
    
    if suit_match_count > 0:
        available_suit = [c for c in suit_match_cards if c not in reserved_cards]
        selected_suit = random.sample(available_suit, min(suit_match_count, len(available_suit)))
        dead_cards.extend(selected_suit)
        reserved_cards.update(selected_suit)
    
    suited_over_count = 0
    for card in dead_cards:
        if card[0] in ranks[:high_idx] and card[1] == first_card_suit:
            suited_over_count += 1
    
    remaining_over_cards_needed = over_cards - suited_over_count
    
    available_over = [c for c in over_cards_pool if c not in reserved_cards]
    if suit_match_count > 0:
        available_over = [c for c in available_over if c[1] != first_card_suit]
    
    num_over_to_add = min(remaining_over_cards_needed, len(available_over), remaining_dead_cards)
    if num_over_to_add > 0:
        selected_over = random.sample(available_over, num_over_to_add)
        dead_cards.extend(selected_over)
        reserved_cards.update(selected_over)
    
    remaining_dead_cards = num_dead_cards - len(dead_cards)
    if remaining_dead_cards > 0:
        available_lower = [c for c in lower_cards_pool if c not in reserved_cards]
        if suit_match_count > 0:
            available_lower = [c for c in available_lower if c[1] != first_card_suit]
        num_lower_to_add = min(remaining_dead_cards, len(available_lower))
        if num_lower_to_add > 0:
            selected_lower = random.sample(available_lower, num_lower_to_add)
            dead_cards.extend(selected_lower)
            reserved_cards.update(selected_lower)
    
    remaining_dead_cards = num_dead_cards - len(dead_cards)
    if remaining_dead_cards > 0:
        all_remaining = [c for c in (over_cards_pool + lower_cards_pool) if c not in reserved_cards]
        if suit_match_count > 0:
            all_remaining = [c for c in all_remaining if c[1] != first_card_suit]
        num_final = min(remaining_dead_cards, len(all_remaining))
        if num_final > 0:
            selected_final = random.sample(all_remaining, num_final)
            dead_cards.extend(selected_final)
    
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
        low_rank = min(player_ranks, key=lambda r: ranks.index(r))
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
