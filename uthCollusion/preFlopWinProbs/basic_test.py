from uthCollusion.preFlopWinProbs.uthSimulation import checkOdds


def run_basic_tests():
    """Run basic test cases for validation."""
    
    print("=" * 80)
    print("BASIC TESTS")
    print("=" * 80)
    
    # Test case 1: Pair of Aces
    print("Test Case 1: Pair of Aces")
    aces_hand = ['As', 'Ah']
    result = checkOdds(aces_hand)
    print(f"Win Rate: {result['win_rate']:.3f}")
    print(f"Loss Rate: {result['loss_rate']:.3f}")
    print(f"Tie Rate: {result['tie_rate']:.3f}")
    print()
    
    # Test case 2: J and 9
    print("Test Case 2: J and 9")
    j9_hand = ['Jh', '9c']
    result = checkOdds(j9_hand)
    print(f"Win Rate: {result['win_rate']:.3f}")
    print(f"Loss Rate: {result['loss_rate']:.3f}")
    print(f"Tie Rate: {result['tie_rate']:.3f}")
    print()
    
    # Test case 3: 2 and 7 offsuit
    print("Test Case 3: 2 and 7 offsuit")
    trash_hand = ['2h', '7c']
    result = checkOdds(trash_hand)
    print(f"Win Rate: {result['win_rate']:.3f}")
    print(f"Loss Rate: {result['loss_rate']:.3f}")
    print(f"Tie Rate: {result['tie_rate']:.3f}")
    print()
    
    # Test case 4: J and 9 with dead face cards
    print("Test Case 4: J and 9 with dead face cards")
    def dead_face_cards():
        return ['Kc', 'Kd', 'Kh', 'Ks', 'Qc', 'Qd', 'Qh', 'Qs','Ac', 'Ad', 'Ah', 'As']
    
    result = checkOdds(j9_hand, dead_face_cards)
    print(f"Win Rate: {result['win_rate']:.3f}")
    print(f"Loss Rate: {result['loss_rate']:.3f}")
    print(f"Tie Rate: {result['tie_rate']:.3f}")
    print("This should be higher than the J9 win rate without dead cards")
    print()


def main():
    """Main function to run basic tests."""
    run_basic_tests()


if __name__ == "__main__":
    main()