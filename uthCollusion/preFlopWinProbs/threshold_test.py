from uthCollusion.preFlopWinProbs.uthSimulation import checkOdds
from uthCollusion.preFlopWinProbs.dead_card import create_unified_dead_cards_fn


def find_lowest_winning_hand(start_high_card='J', start_low_card='9', num_higher_cards=None, num_simulations=5000):
    """
    Find the lowest hand that still has >50% win rate.
    Starts from specified cards and goes down each time.
    Continues testing until reaching the 2 or finding a losing hand.
    
    Returns:
        dict: Structured result with all tested hands and lowest winning hand
    """
    ranks = ['A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2']
    suits = ['h', 'c']  # Using hearts and clubs to avoid same suit issues
    
    # Find starting positions
    high_idx = ranks.index(start_high_card)
    low_idx = ranks.index(start_low_card)
    
    # Generate all hands to test in proper sequence
    hands_to_test = []
    
    for i in range(high_idx, len(ranks)):
        for j in range(i + 1, len(ranks)):  # j > i ensures lower card
            hand = [ranks[i] + suits[0], ranks[j] + suits[1]]
            hands_to_test.append(hand)
    
    # Test hands sequentially and collect results
    hands_tested = []
    lowest_winning_hand = None
    lowest_winning_rate = 0
    found_losing_hand = False
    
    for hand in hands_to_test:
        # Evaluate this hand
        if num_higher_cards is None:
            result = checkOdds(hand, None, simulations=num_simulations)
        else:
            hand_generator = create_unified_dead_cards_fn(over_cards=num_higher_cards, playerHand=hand)
            if hand_generator is None:
                continue
            result = checkOdds(hand, hand_generator, simulations=num_simulations)
        
        final_win_rate = result['win_rate']
        total_sims = result['total_simulations']
        
        # Determine if this is a winning hand
        is_winning = final_win_rate > 0.50
        
        # Add to results
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
    
    # Return structured result
    return {
        'lowest_winning_hand': lowest_winning_hand,
        'lowest_winning_rate': lowest_winning_rate,
        'hands_tested': hands_tested,
        'total_hands_tested': len(hands_tested),
        'start_cards': [start_high_card, start_low_card],
        'num_higher_cards': num_higher_cards
    }


def run_single_threshold_test(start_high_card, start_low_card, num_higher_cards=None, num_simulations=5000, verbose=False):
    """Run a single threshold test and return structured results."""
    import time
    
    start_time = time.time()
    result = find_lowest_winning_hand(start_high_card, start_low_card, num_higher_cards, num_simulations)
    execution_time = time.time() - start_time
    
    return {
        'test_name': f"{'No Dead Cards' if num_higher_cards is None else f'{num_higher_cards} Higher Cards'}",
        'result': result,
        'execution_time': execution_time
    }


def run_all_threshold_tests(start_high_card='J', start_low_card='9', num_simulations=5000, verbose=False):
    """Run all threshold tests concurrently and return structured results."""
    import concurrent.futures
    import time
    
    test_configs = [
        {'num_higher_cards': None, 'name': 'No Dead Cards'},
        {'num_higher_cards': 6, 'name': '6 Higher Cards + 4 Lower Cards Dead'},
        {'num_higher_cards': 3, 'name': '3 Higher Cards + 7 Lower Cards Dead'}
    ]
    
    start_time = time.time()
    
    # Run all tests concurrently using ThreadPoolExecutor
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        future_to_config = {
            executor.submit(run_single_threshold_test, start_high_card, start_low_card, config['num_higher_cards'], num_simulations, verbose): config
            for config in test_configs
        }
        
        results = []
        for future in concurrent.futures.as_completed(future_to_config):
            config = future_to_config[future]
            try:
                result = future.result()
                result['test_name'] = config['name']
                results.append(result)
            except Exception as e:
                if verbose:
                    print(f"Error in {config['name']}: {e}")
    
    total_time = time.time() - start_time
    
    return {
        'start_cards': [start_high_card, start_low_card],
        'total_execution_time': total_time,
        'test_results': results,
        'summary': {
            'total_tests': len(results),
            'successful_tests': len([r for r in results if r['result']['lowest_winning_hand']])
        }
    }


def print_threshold_results(results, verbose=False):
    """Print formatted threshold test results from structured data."""
    if not verbose:
        return
    
    print("=" * 80)
    print("THRESHOLD TESTS: Finding Lowest Hands with >50% Win Rate")
    print(f"Starting from {results['start_cards'][0]}{results['start_cards'][1]}")
    print("=" * 80)
    print()
    
    # Print each test result
    for i, test_result in enumerate(results['test_results'], 1):
        print(f"TEST {i}: {test_result['test_name']}")
        
        # Show sample dead cards if applicable
        if test_result['result']['num_higher_cards'] is not None:
            player_hand = [results['start_cards'][0] + 'h', results['start_cards'][1] + 'c']
            dead_gen = create_unified_dead_cards_fn(over_cards=test_result['result']['num_higher_cards'], playerHand=player_hand)
            if dead_gen is None:
                print("Sample dead cards: (impossible scenario)")
            else:
                dead_cards = dead_gen()
                if dead_cards:
                    print(f"Sample dead cards: {', '.join(sorted(dead_cards[:10]))}{'...' if len(dead_cards) > 10 else ''}")
        
        print("-" * 60)
        
        # Print all tested hands
        for hand_data in test_result['result']['hands_tested']:
            hand = hand_data['hand']
            win_rate = hand_data['win_rate']
            total_sims = hand_data['total_simulations']
            is_winning = hand_data['is_winning']
            
            if total_sims > 5000:
                if is_winning:
                    print(f"{hand[0]}{hand[1]}: Win Rate = {win_rate:.3f} (ran {total_sims:,} simulations)")
                else:
                    print(f"{hand[0]}{hand[1]}: Win Rate = {win_rate:.3f} (ran {total_sims:,} simulations, below 50%)")
            else:
                if is_winning:
                    print(f"{hand[0]}{hand[1]}: Win Rate = {win_rate:.3f}")
                else:
                    print(f"{hand[0]}{hand[1]}: Win Rate = {win_rate:.3f} (below 50%)")
        
        print("-" * 60)
        if test_result['result']['lowest_winning_hand']:
            lowest_hand = test_result['result']['lowest_winning_hand']
            lowest_rate = test_result['result']['lowest_winning_rate']
            print(f"Lowest winning hand: {lowest_hand[0]}{lowest_hand[1]} with {lowest_rate:.3f} win rate")
        else:
            print("No hand found with >50% win rate")
        print(f"⏱️  Test {i} completed in {test_result['execution_time']:.2f} seconds")
        print()
    
    # Summary
    print("=" * 80)
    print("TIMING SUMMARY")
    for i, test_result in enumerate(results['test_results'], 1):
        print(f"Test {i} ({test_result['test_name']}):    {test_result['execution_time']:6.2f} seconds")
    print(f"Total time:                 {results['total_execution_time']:6.2f} seconds")
    print("=" * 80)


def main():
    """Main function with configuration options."""
    import sys
    
    # Parse command line arguments
    start_card = 'J'
    start_low = '9'
    num_simulations = 5000
    verbose = False
    
    i = 1
    while i < len(sys.argv):
        arg = sys.argv[i].lower()
        if arg == '--start-card' and i + 1 < len(sys.argv):
            start_card = sys.argv[i + 1].upper()
            i += 1
        elif arg == '--start-low' and i + 1 < len(sys.argv):
            start_low = sys.argv[i + 1].upper()
            i += 1
        elif arg in ['--simulations', '-n'] and i + 1 < len(sys.argv):
            num_simulations = int(sys.argv[i + 1])
            i += 1
        elif arg in ['--verbose', '-v']:
            verbose = True
        elif arg in ['--help', '-h']:
            print("Usage: python threshold_test.py [options]")
            print("Options:")
            print("  --start-card CARD      Starting high card (default: J)")
            print("  --start-low CARD        Starting low card (default: 9)")
            print("  --simulations, -n NUM  Number of simulations per scenario (default: 5000)")
            print("  --verbose, -v           Print verbose output")
            print("  --help, -h              Show this help message")
            return
        else:
            print(f"Unknown argument: {arg}")
            print("Use --help for usage information")
            return
        i += 1
    
    # Run all threshold tests and print results
    results = run_all_threshold_tests(start_card, start_low, num_simulations, verbose)
    print_threshold_results(results, verbose)


if __name__ == "__main__":
    main()
