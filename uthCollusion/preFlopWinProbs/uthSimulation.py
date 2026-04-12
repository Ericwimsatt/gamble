import random
import os
from typing import List, Tuple, Callable, Optional
from treys import Card, Evaluator, Deck

class UltimateTexasHoldemSimulator:
    def __init__(self):
        self.evaluator = Evaluator()
        
    def create_deck(self, player_hand: List[str], dead_cards_fn: Optional[Callable[[], Optional[List[str]]]] = None) -> List[str]:
        """Create a deck with player hand and dead cards removed."""
        full_deck = Deck.GetFullDeck()
        # Convert to string representation
        deck_strings = [Card.int_to_str(card) for card in full_deck]
        
        # Remove player cards
        for card in player_hand:
            if card in deck_strings:
                deck_strings.remove(card)
        
        # Remove dead cards
        if dead_cards_fn:
            dead_cards = dead_cards_fn()
            if dead_cards:
                for card in dead_cards:
                    if card in deck_strings:
                        deck_strings.remove(card)
                    
        return deck_strings
    
    def evaluate_hand(self, player_hand: List[str], community_cards: List[str]) -> Tuple[int, str]:
        """Evaluate hand strength using Treys evaluator."""
        # Convert string cards to integers for Treys
        player_cards = [Card.new(card) for card in player_hand]
        community_cards_int = [Card.new(card) for card in community_cards]
        
        # Evaluate hand
        hand_rank = self.evaluator.evaluate(player_cards, community_cards_int)
        hand_class = self.evaluator.get_rank_class(hand_rank)
        
        return hand_rank, self.evaluator.class_to_string(hand_class)
    
    def simulate_game(self, player_hand: List[str], dead_cards_fn: Optional[Callable[[], Optional[List[str]]]] = None, 
                     simulations: int = 10000) -> dict:
        """Run Monte Carlo simulation for Ultimate Texas Hold'em."""
        wins = 0
        losses = 0
        ties = 0
        dealer_qualifies_count = 0
        
        for _ in range(simulations):
            # Create deck with player hand and dead cards removed
            remaining_deck = self.create_deck(player_hand, dead_cards_fn)
            random.shuffle(remaining_deck)
            
            # Deal 5 community cards
            community_cards = remaining_deck[:5]
            
            # Deal 2 cards to dealer
            dealer_hand = remaining_deck[5:7]
            
            # Evaluate hands
            player_rank, _ = self.evaluate_hand(player_hand, community_cards)
            dealer_rank, _ = self.evaluate_hand(dealer_hand, community_cards)
            
            # Check if dealer qualifies (pair of 4s or better in Ultimate Texas Hold'em)
            dealer_cards_int = [Card.new(card) for card in dealer_hand]
            community_cards_int = [Card.new(card) for card in community_cards]
            dealer_qualifies_rank = self.evaluator.evaluate(dealer_cards_int, community_cards_int)
            dealer_hand_class = self.evaluator.get_rank_class(dealer_qualifies_rank)
            dealer_qualifies = dealer_hand_class <= 2  # Pair or better (simplified)
            
            if dealer_qualifies:
                dealer_qualifies_count += 1
            
            # Determine winner
            if player_rank < dealer_rank:
                wins += 1
            elif player_rank > dealer_rank:
                losses += 1
            else:
                ties += 1
        
        total = wins + losses + ties
        win_rate = wins / total if total > 0 else 0
        loss_rate = losses / total if total > 0 else 0
        tie_rate = ties / total if total > 0 else 0
        qualify_rate = dealer_qualifies_count / simulations if simulations > 0 else 0
        
        return {
            'win_rate': win_rate,
            'loss_rate': loss_rate,
            'tie_rate': tie_rate,
            'dealer_qualify_rate': qualify_rate,
            'total_simulations': simulations
        }


def checkOdds(player_hand: List[str], dead_cards_fn: Optional[Callable[[], Optional[List[str]]]] = None, 
              simulations: int = 10000) -> dict:
    """
    Convenience function to calculate odds for a given hand.
    Automatically increases simulations if result is close to 50% threshold.
    
    Args:
        player_hand: List of 2 cards in player's hand
        dead_cards_fn: Optional function that returns list of dead cards
        simulations: Initial number of Monte Carlo simulations to run
        
    Returns:
        Dictionary with win_rate, loss_rate, tie_rate, dealer_qualify_rate, and total_simulations
    """
    simulator = UltimateTexasHoldemSimulator()
    result = simulator.simulate_game(player_hand, dead_cards_fn, simulations)
    
    # If win rate is within 0.01 of 0.500, run more simulations for accuracy
    if abs(result['win_rate'] - 0.500) <= 0.01:
        additional_sims = simulations * 4 # Run additional simulations
        
        # Run additional simulations and combine results
        additional_result = simulator.simulate_game(player_hand, dead_cards_fn, additional_sims)
        
        # Combine results weighted by simulation count
        total_sims = simulations + additional_sims
        combined_wins = (result['win_rate'] * simulations + additional_result['win_rate'] * additional_sims)
        combined_losses = (result['loss_rate'] * simulations + additional_result['loss_rate'] * additional_sims)
        combined_ties = (result['tie_rate'] * simulations + additional_result['tie_rate'] * additional_sims)
        combined_qualifies = (result['dealer_qualify_rate'] * simulations + additional_result['dealer_qualify_rate'] * additional_sims)
        
        result = {
            'win_rate': combined_wins / total_sims,
            'loss_rate': combined_losses / total_sims,
            'tie_rate': combined_ties / total_sims,
            'dealer_qualify_rate': combined_qualifies / total_sims,
            'total_simulations': total_sims
        }
    
    return result


