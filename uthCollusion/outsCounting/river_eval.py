import treys

def count_pair_and_high_card_categories(player_cards: list[int], shared_cards: list[int]) -> dict:
    player_ranks = sorted([treys.Card.get_rank_int(c) for c in player_cards])
    low_rank, high_rank = player_ranks

    counts = {
        "overCardCount": 0,
        "highPairCount": 0,
        "betweenCount": 0,
        "lowPairCount": 0,
        "underCardCount": 0
    }

    for card in shared_cards:
        rank = treys.Card.get_rank_int(card)
        if rank > high_rank:
            counts["overCardCount"] += 1
        elif rank == high_rank:
            counts["highPairCount"] += 1
        elif rank > low_rank:
            counts["betweenCount"] += 1
        elif rank == low_rank:
            counts["lowPairCount"] += 1
        else:
            counts["underCardCount"] += 1

    return counts

def get_remaining_cards(player_cards: list[int], shared_cards: list[int]) -> set[int]:
    full_deck = set(treys.Deck.GetFullDeck())
    used_cards = set(player_cards) | set(shared_cards)
    return full_deck - used_cards

def max_super(a,b):
    if a>b:
        return a,0
    if b>a:
        return b,1
    return a,0

def enumerate_pair_and_high_card_outs(player_cards: list[int], shared_cards: list[int]) -> list[tuple[int, int]]:

    outs = []
    
    counts = count_pair_and_high_card_categories(player_cards, shared_cards)
    player_ranks = sorted([treys.Card.get_rank_int(c) for c in player_cards], reverse=True)
    shared_ranks = sorted([treys.Card.get_rank_int(c) for c in shared_cards], reverse=True)
    player_high_rank, player_low_rank = player_ranks
    if player_high_rank == player_low_rank:
        counts["highPairCount"] += 1
    remaining_cards = get_remaining_cards(player_cards, shared_cards)
    maxCount, maxIndex = max_super(counts["highPairCount"], counts["lowPairCount"])
    totalPairs = counts["highPairCount"] + counts["lowPairCount"]
    maxPairValue = player_ranks[maxIndex]

    # if royal_flush->full house->quads->flush->straight->trips->two pair->pair->high card
    # eval dealer hand against each player hand.
    #DKLMKL
    if totalPairs == 1:
        dealer_board_pairs = {
            "higherPair":[],
            "samePair":[],
            "lowerPair":[]
        }

        for card in remaining_cards:
            rank = treys.Card.get_rank_int(card)
            if rank in shared_ranks:
            #TODO: trips is also a higher pair because we're only looking when player has 1 pair
                if rank > maxPairValue:
                    dealer_board_pairs["higherPair"].append(card)
                elif rank == maxPairValue:
                    dealer_board_pairs["samePair"].append(card)
                elif rank < maxPairValue:
                    dealer_board_pairs["lowerPair"].append(card)
        
        for higher_pair_card in dealer_board_pairs["higherPair"]:
            remaining_cards.remove(higher_pair_card)
            for card in remaining_cards:
                outs.append((higher_pair_card, card))

        for same_pair_card in dealer_board_pairs["samePair"]:
            remaining_cards.remove(same_pair_card)
            for card in remaining_cards:
                #trips
                if treys.Card.get_rank_int(card) == treys.Card.get_rank_int(same_pair_card):
                    outs.append((same_pair_card, card))
                    continue
                #2 pair
                elif card in dealer_board_pairs["lowerPair"]:
                    outs.append((same_pair_card, card))
                elif treys.Card.get_rank_int(card) > player_low_rank:
                    outs.append((same_pair_card, card))

        for lower_pair_card in dealer_board_pairs["lowerPair"]:
            remaining_cards.remove(lower_pair_card)
            for card in remaining_cards:
                 #trips
                if treys.Card.get_rank_int(card) == treys.Card.get_rank_int(same_pair_card):
                    outs.append((same_pair_card, card))
                    continue
                #2 pair
                if card in dealer_board_pairs["lowerPair"]:
                    outs.append((lower_pair_card, card))
    
    print("OUTS")
    for hand in outs:
        print(f"{treys.Card.int_to_pretty_str(hand[0])}, {treys.Card.int_to_pretty_str(hand[1])}")
    return sorted(set(outs))

if __name__ == "__main__":
    player_cards = [treys.Card.new("Ah"), treys.Card.new("Kh")]
    shared_cards = [treys.Card.new("As"), treys.Card.new("Js"), treys.Card.new("Jc"), treys.Card.new("6c"), treys.Card.new("2s")]
    result = enumerate_pair_and_high_card_outs(player_cards, shared_cards)
    #This should include every tuple of a dealer's hand that would beat the player.
    assert (treys.Card.new("Ac"), treys.Card.new("Jd")) in result
    assert (treys.Card.new("Ah"), treys.Card.new("Ts")) in result
    remaining_cards = get_remaining_cards(player_cards, shared_cards)
    assert len(remaining_cards) == 45
    for card in remaining_cards:
        if card is not treys.Card.new("Jd"):
            assert (treys.Card.new("Jd"), card) in result
    assert len(result) == 94