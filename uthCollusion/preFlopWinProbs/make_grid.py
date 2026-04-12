import threading
import concurrent.futures
import time
from typing import List, Optional, Dict, Callable
from uthCollusion.preFlopWinProbs.dead_card import (
    find_lowest_winning_hand,
    create_unified_dead_cards_fn,
    RANKS,
    SUITS,
)

SCENARIOS = {
    'no_match': {
        'name': 'No dead cards match player hand values',
        'suit_match_count': 0,
        'upper_pair_count': 0,
        'lower_pair_count': 0,
    },
    'match_high': {
        'name': 'Exactly 1 dead card matches high card value',
        'suit_match_count': 0,
        'upper_pair_count': 1,
        'lower_pair_count': 0,
    },
    'match_low': {
        'name': 'Exactly 1 dead card matches low card value',
        'suit_match_count': 0,
        'upper_pair_count': 0,
        'lower_pair_count': 1,
    },
    'suited_no_hearts': {
        'name': 'Both player cards are hearts, no dead hearts',
        'suit_match_count': 0,
        'upper_pair_count': 0,
        'lower_pair_count': 0,
    },
    'suited_4_hearts': {
        'name': 'Both player cards are hearts, 4 dead hearts',
        'suit_match_count': 4,
        'upper_pair_count': 0,
        'lower_pair_count': 0,
    },
    'suited_6_hearts': {
        'name': 'Both player cards are hearts, 6 dead hearts',
        'suit_match_count': 6,
        'upper_pair_count': 0,
        'lower_pair_count': 0,
    },
}

GRID_HIGH_CARDS = ['A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6']
GRID_OVER_CARDS = list(range(11))


def find_threshold_for_cell(high_card: str, num_over_cards: int, scenario_key: str, num_simulations: int, verbose: bool = False) -> tuple:
    """Find the threshold (lowest winning second card) for a single cell."""
    scenario = SCENARIOS[scenario_key]
    
    if verbose:
        print(f"  Processing {high_card} with {num_over_cards} over cards, scenario: {scenario_key}")
    
    player_high = high_card
    player_low = '9'
    
    if scenario_key.startswith('suited'):
        player_hand = [player_high + 'h', player_low + 'h']
    else:
        player_hand = [player_high + 'h', player_low + 'c']
    
    dead_cards_fn = create_unified_dead_cards_fn(
        num_dead_cards=10,
        over_cards=num_over_cards,
        playerHand=player_hand,
        suit_match_count=scenario.get('suit_match_count', 0),
        upper_pair_count=scenario.get('upper_pair_count', 0),
        lower_pair_count=scenario.get('lower_pair_count', 0),
    )
    
    if dead_cards_fn is None:
        return ('-', None)
    
    test_dead_cards = dead_cards_fn()
    if test_dead_cards is None:
        return ('-', None)
    
    result = find_lowest_winning_hand(
        start_high_card=player_high,
        start_low_card=player_low,
        dead_cards_fn=dead_cards_fn,
        num_simulations=num_simulations
    )
    
    if result['lowest_winning_hand'] is None:
        return ('X', None)
    
    lowest_hand = result['lowest_winning_hand']
    low_card_value = lowest_hand[1][0]
    win_rate = result['lowest_winning_rate']
    
    if verbose:
        print(f"    Result: {low_card_value} (win rate: {win_rate:.3f})")
    
    return (low_card_value, win_rate)


def generate_row(high_card: str, scenario_key: str, num_simulations: int, verbose: bool = False, row_lock: Optional[threading.Lock] = None) -> List[tuple]:
    """Generate a single row of the grid."""
    row = []
    
    if verbose:
        print(f"Starting row for {high_card}")
    
    for num_over in GRID_OVER_CARDS:
        result = find_threshold_for_cell(high_card, num_over, scenario_key, num_simulations, verbose)
        row.append(result)
    
    return row


def generate_grid(scenario_key: Optional[str] = None, high_card: Optional[str] = None, num_simulations: int = 1000, verbose: bool = False, max_workers: int = 8) -> Dict:
    """Generate the complete grid or a single row."""
    start_time = time.time()
    
    scenarios_to_run = [scenario_key] if scenario_key else list(SCENARIOS.keys())
    
    if high_card:
        high_cards_to_run = [high_card]
    else:
        high_cards_to_run = GRID_HIGH_CARDS
    
    total_cells = len(scenarios_to_run) * len(high_cards_to_run) * len(GRID_OVER_CARDS)
    
    processed_cells = [0]
    progress_lock = threading.Lock()
    
    if verbose:
        print(f"Total cells to process: {total_cells}")
    
    results = {}
    
    for scen_key in scenarios_to_run:
        if verbose:
            print(f"\n=== Scenario: {SCENARIOS[scen_key]['name']} ===")
        
        results[scen_key] = {}
        row_results = {}
        
        def generate_row_wrapper(hc):
            result = generate_row(hc, scen_key, num_simulations, verbose)
            with progress_lock:
                processed_cells[0] += len(GRID_OVER_CARDS)
                print(f"\rProgress: {processed_cells[0]}/{total_cells} cells ({100*processed_cells[0]/total_cells:.1f}%)", end="", flush=True)
            return (hc, result)
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {executor.submit(generate_row_wrapper, hc): hc for hc in high_cards_to_run}
            
            for future in concurrent.futures.as_completed(futures):
                hc, row = future.result()
                row_results[hc] = row
        
        for hc in high_cards_to_run:
            results[scen_key][hc] = row_results[hc]
    
    print()  # newline after progress
    execution_time = time.time() - start_time
    
    return {
        'results': results,
        'scenarios': scenarios_to_run,
        'high_cards': high_cards_to_run,
        'num_simulations': num_simulations,
        'execution_time': execution_time,
        'verbose': verbose
    }


def print_grid(results: Dict, verbose: bool = False):
    """Print the grid results."""
    if not verbose:
        print("\n" + "=" * 80)
    
    for scen_key in results['scenarios']:
        scenario_name = SCENARIOS[scen_key]['name']
        
        if not verbose:
            print(f"\n{scenario_name}")
            print("-" * 60)
        else:
            print(f"\n{'=' * 80}")
            print(f"Scenario: {scenario_name}")
            print(f"Execution time: {results['execution_time']:.2f} seconds")
        
        header = "  " + " ".join(f"{x:>3}" for x in GRID_OVER_CARDS)
        if not verbose:
            print("\nLowest 2nd card to play:")
            print(header)
        
        for hc in results['high_cards']:
            row = results['results'][scen_key][hc]
            row_str = " ".join(f"{x[0]:>3}" for x in row)
            if not verbose:
                print(f"{hc} {row_str}")
        
        if not verbose:
            print("\nWin % with recommended hand:")
            print(header)
        
        for hc in results['high_cards']:
            row = results['results'][scen_key][hc]
            row_str = " ".join(f"{x[1]*100:>6.2f}" if x[1] is not None else "   -  " for x in row)
            if not verbose:
                print(f"{hc} {row_str}")
        
        if not verbose:
            print()


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Generate winning threshold grids for poker hands')
    parser.add_argument('--scenario', '-s', type=str, choices=list(SCENARIOS.keys()), 
                        help='Run specific scenario (default: all scenarios)')
    parser.add_argument('--high-card', type=str, choices=GRID_HIGH_CARDS,
                        help='Run specific row by high card (default: all rows)')
    parser.add_argument('--simulations', '-n', type=int, default=1000,
                        help='Number of Monte Carlo simulations per cell (default: 1000)')
    parser.add_argument('--verbose', '-v', action='store_true',
                        help='Enable verbose debug output')
    parser.add_argument('--workers', '-w', type=int, default=8,
                        help='Maximum number of worker threads (default: 8)')
    
    args = parser.parse_args()
    
    if args.verbose:
        print(f"Running with {args.simulations} simulations per cell")
        print(f"Scenario: {args.scenario if args.scenario else 'all'}")
        print(f"High card: {args.high_card if args.high_card else 'all'}")
    
    results = generate_grid(
        scenario_key=args.scenario,
        high_card=args.high_card,
        num_simulations=args.simulations,
        verbose=args.verbose,
        max_workers=args.workers
    )
    
    print_grid(results, verbose=args.verbose)
    
    if args.verbose:
        print(f"\nTotal execution time: {results['execution_time']:.2f} seconds")


if __name__ == "__main__":
    main()
