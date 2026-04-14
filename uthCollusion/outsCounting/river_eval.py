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

def enumerate_pair_and_high_card_outs(player_cards: list[int], shared_cards: list[int]) -> list[int]:
    counts = count_pair_and_high_card_categories(player_cards, shared_cards)
    outs = []
    
    # Add overcards
    if counts["overCardCount"] > 0:
        outs.extend([c for c in range(2, 15) if c > max(player_cards)])
    
    # Add high pair outs
    if counts["highPairCount"] > 0:
        outs.append(max(player_cards))
    
    # Add between cards
    if counts["betweenCount"] > 0:
        low_rank, high_rank = sorted([treys.Card.get_rank_int(c) for c in player_cards])
        outs.extend([c for c in range(low_rank + 1, high_rank)])
    
    # Add low pair outs
    if counts["lowPairCount"] > 0:
        outs.append(min(player_cards))
    
    return sorted(set(outs))