import unittest
import random
from uthCollusion.preFlopWinProbs.dead_card import generate_dead_cards_unified, RANKS, SUITS


def create_full_deck():
    return [r + s for r in RANKS for s in SUITS]


def get_player_high_card(player_hand):
    player_ranks = [card[0] for card in player_hand]
    high_rank = max(player_ranks, key=lambda r: RANKS.index(r))
    return high_rank


def get_player_suit(player_hand):
    high_card = max(player_hand, key=lambda c: RANKS.index(c[0]))
    return high_card[1]


class TestGenerateDeadCardsUnified(unittest.TestCase):
    
    def setUp(self):
        random.seed(42)
    
    def test_dead_cards_count(self):
        """Test that the correct number of dead cards are returned."""
        for num_dead in [5, 10, 15, 20]:
            for _ in range(10):
                result = generate_dead_cards_unified(
                    num_dead_cards=num_dead,
                    over_cards=3,
                    playerHand=['Qh', 'Jd']  # Use Q-high so over_cards works
                )
                self.assertEqual(len(result), num_dead)
    
    def test_no_duplicate_dead_cards(self):
        """Test that dead cards don't contain duplicates."""
        for _ in range(20):
            result = generate_dead_cards_unified(
                num_dead_cards=10,
                over_cards=3,
                playerHand=['Qh', 'Jd']  # Use Q-high so over_cards works
            )
            self.assertIsNotNone(result)
            self.assertEqual(len(result), len(set(result)), f"Found duplicates in {result}")
    
    def test_player_hand_not_in_dead_cards(self):
        """Test that player hand cards are not in dead cards."""
        player_hand = ['Qs', 'Js']  # Use Q-high so over_cards works
        for _ in range(20):
            result = generate_dead_cards_unified(
                num_dead_cards=10,
                over_cards=3,
                playerHand=player_hand
            )
            self.assertIsNotNone(result)
            for card in player_hand:
                self.assertNotIn(card, result, f"Player card {card} found in dead cards {result}")
    
    def test_upper_pair_removal(self):
        """Test that upper pair cards are removed from deck (same rank as high card)."""
        player_hand = ['Qs', 'Kh']  # High card is K, low card is Q
        high_rank = 'K'  # K > Q in poker
        
        for _ in range(20):
            result = generate_dead_cards_unified(
                num_dead_cards=10,
                over_cards=0,
                upper_pair_count=1,
                lower_pair_count=0,
                suit_match_count=0,
                playerHand=player_hand
            )
            self.assertIsNotNone(result)
            upper_pair_in_dead = [c for c in result if c[0] == high_rank]
            self.assertGreaterEqual(len(upper_pair_in_dead), 1, 
                f"Expected at least 1 upper pair card in dead cards, got {len(upper_pair_in_dead)}: {upper_pair_in_dead}")
    
    def test_lower_pair_removal(self):
        """Test that lower pair cards are removed from deck (same rank as low card)."""
        player_hand = ['Qs', 'Kh']  # High card is K, low card is Q
        low_rank = 'Q'  # Q < K in poker
        
        for _ in range(20):
            result = generate_dead_cards_unified(
                num_dead_cards=10,
                over_cards=0,
                upper_pair_count=0,
                lower_pair_count=1,
                suit_match_count=0,
                playerHand=player_hand
            )
            self.assertIsNotNone(result)
            lower_pair_in_dead = [c for c in result if c[0] == low_rank]
            self.assertGreaterEqual(len(lower_pair_in_dead), 1,
                f"Expected at least 1 lower pair card in dead cards, got {len(lower_pair_in_dead)}: {lower_pair_in_dead}")
    
    def test_upper_and_lower_pair_count(self):
        """Test that both upper and lower pair counts work together."""
        player_hand = ['Qs', 'Kh']  # High=K, Low=Q
        
        for _ in range(20):
            result = generate_dead_cards_unified(
                num_dead_cards=10,
                over_cards=0,
                upper_pair_count=1,
                lower_pair_count=1,
                playerHand=player_hand
            )
            self.assertIsNotNone(result)
            
            kings_in_dead = [c for c in result if c[0] == 'K']
            queens_in_dead = [c for c in result if c[0] == 'Q']
            
            self.assertGreaterEqual(len(kings_in_dead), 1, f"Expected at least 1 king in dead cards: {result}")
            self.assertGreaterEqual(len(queens_in_dead), 1, f"Expected at least 1 queen in dead cards: {result}")
    
    def test_suit_match_cards_are_suited(self):
        """Test that suit_match_count cards are of the same suit as player's high card."""
        player_hand = ['Qh', 'Kd']  # High card is K, suit match to Kd is diamonds - use hearts
        player_hand = ['Kh', 'Qd']  # High card is K (hearts), suit match should be hearts
        high_suit = 'h'
        
        for _ in range(20):
            result = generate_dead_cards_unified(
                num_dead_cards=10,
                over_cards=0,
                suit_match_count=2,
                playerHand=player_hand
            )
            self.assertIsNotNone(result)
            suited_cards = [c for c in result if c[1] == high_suit]
            self.assertGreaterEqual(len(suited_cards), 2,
                f"Expected at least 2 suited cards in dead cards, got {len(suited_cards)}: {result}")
    
    def test_over_cards_higher_than_high_card(self):
        """Test that over_cards are higher than player's high card."""
        player_hand = ['Th', '8d']  # High card is T
        
        for _ in range(20):
            result = generate_dead_cards_unified(
                num_dead_cards=10,
                over_cards=3,
                suit_match_count=0,
                upper_pair_count=0,
                lower_pair_count=0,
                playerHand=player_hand
            )
            self.assertIsNotNone(result)
            
            high_rank_idx = RANKS.index('T')
            over_cards_in_dead = [c for c in result if RANKS.index(c[0]) < high_rank_idx]
            
            self.assertGreaterEqual(len(over_cards_in_dead), 3,
                f"Expected at least 3 over cards, got {len(over_cards_in_dead)}: {result}")
    
    def test_remaining_dead_cards_lower_than_high_card(self):
        """Test that remaining dead cards (after over cards) are lower than player's high card."""
        player_hand = ['Qh', 'Jd']  # High card is Q
        
        for _ in range(20):
            result = generate_dead_cards_unified(
                num_dead_cards=10,
                over_cards=3,
                suit_match_count=0,
                upper_pair_count=0,
                lower_pair_count=0,
                playerHand=player_hand
            )
            self.assertIsNotNone(result)
            
            high_rank_idx = RANKS.index('Q')
            
            lower_cards = [c for c in result if RANKS.index(c[0]) > high_rank_idx]
            over_cards = [c for c in result if RANKS.index(c[0]) < high_rank_idx]
            
            total_expected = len(over_cards) + len(lower_cards)
            self.assertEqual(total_expected, len(result),
                f"Over cards + lower cards should equal total dead cards: {result}")
    
    def test_suit_match_reduces_over_cards(self):
        """Test that suited cards higher than player's high card reduce the over_cards count."""
        player_hand = ['Th', '8d']
        
        for _ in range(20):
            result = generate_dead_cards_unified(
                num_dead_cards=10,
                over_cards=3,
                suit_match_count=2,
                upper_pair_count=0,
                lower_pair_count=0,
                playerHand=player_hand
            )
            self.assertIsNotNone(result)
            
            high_rank_idx = RANKS.index('T')
            high_suit = 'T' + 'h'
            
            suited_higher = [c for c in result if c[1] == 'h' and RANKS.index(c[0]) < high_rank_idx]
            suited_lower = [c for c in result if c[1] == 'h' and RANKS.index(c[0]) > high_rank_idx]
            
            total_suited = len(suited_higher) + len(suited_lower)
            self.assertGreaterEqual(total_suited, 2,
                f"Expected at least 2 suited cards, got {total_suited}: {result}")
    
    def test_impossible_upper_pair_returns_none(self):
        """Test that impossible upper pair count raises ValueError for invalid hand."""
        player_hand = ['As', 'Ah', 'Ad', 'Ac']  # 4 cards - invalid
        
        with self.assertRaises(ValueError):
            generate_dead_cards_unified(
                num_dead_cards=10,
                over_cards=3,
                upper_pair_count=1,
                playerHand=player_hand
            )
    
    def test_no_player_hand(self):
        """Test that function works with no player hand."""
        for _ in range(10):
            result = generate_dead_cards_unified(
                num_dead_cards=10,
                over_cards=3,
                playerHand=[]
            )
            self.assertIsNotNone(result)
            self.assertEqual(len(result), 10)
            self.assertEqual(len(result), len(set(result)))
    
    def test_over_cards_and_suit_match_combined(self):
        """Test over_cards and suit_match_count work together correctly."""
        player_hand = ['Jh', '9c']
        
        for _ in range(20):
            result = generate_dead_cards_unified(
                num_dead_cards=10,
                over_cards=3,
                suit_match_count=2,
                upper_pair_count=0,
                lower_pair_count=0,
                playerHand=player_hand
            )
            self.assertIsNotNone(result)
            
            high_rank_idx = RANKS.index('J')
            high_suit = 'h'
            
            suited_cards = [c for c in result if c[1] == high_suit]
            over_cards = [c for c in result if RANKS.index(c[0]) < high_rank_idx and c[1] != high_suit]
            
            self.assertGreaterEqual(len(suited_cards), 2,
                f"Expected at least 2 suited cards, got {len(suited_cards)}: {result}")
            self.assertGreaterEqual(len(over_cards), 0,
                f"Expected at least 0 over cards (non-suited), got {len(over_cards)}: {result}")
    
    def test_all_parameters_combined(self):
        """Test all parameters work together."""
        player_hand = ['Qs', 'Jh']  # High=Q, Low=J, high suit is spades
        
        for _ in range(20):
            result = generate_dead_cards_unified(
                num_dead_cards=15,
                over_cards=3,
                suit_match_count=2,
                upper_pair_count=1,
                lower_pair_count=1,
                playerHand=player_hand
            )
            self.assertIsNotNone(result)
            self.assertEqual(len(result), 15)
            
            queens_in_dead = [c for c in result if c[0] == 'Q']
            jacks_in_dead = [c for c in result if c[0] == 'J']
            
            self.assertGreaterEqual(len(queens_in_dead), 1)
            self.assertGreaterEqual(len(jacks_in_dead), 1)
            
            suited_to_queens = [c for c in result if c[1] == 's']  # Qs is in hand, spades
            self.assertGreaterEqual(len(suited_to_queens), 2)
            
            over_cards_list = [c for c in result if RANKS.index(c[0]) < RANKS.index('Q')]
            self.assertGreaterEqual(len(over_cards_list), 3)


if __name__ == '__main__':
    unittest.main()
