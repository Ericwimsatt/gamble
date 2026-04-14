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