
import treys
from river_eval import count_pair_and_high_card_categories, enumerate_pair_and_high_card_outs, get_remaining_cards

def test_pair_category_count():
    player_cards = [treys.Card.new("Ah"), treys.Card.new("9d")]
    shared_cards = [treys.Card.new("As"), treys.Card.new("Kd"), treys.Card.new("7h"), treys.Card.new("5c"), treys.Card.new("2s")]
    result = count_pair_and_high_card_categories(player_cards, shared_cards)
    assert result == {
        "overCardCount": 0,
        "highPairCount": 1,
        "betweenCount": 1,
        "lowPairCount": 0,
        "underCardCount": 3
    }

    player_cards = [treys.Card.new("Jh"), treys.Card.new("6d")]
    shared_cards = [treys.Card.new("As"), treys.Card.new("Kd"), treys.Card.new("7h"), treys.Card.new("5c"), treys.Card.new("2s")]
    result = count_pair_and_high_card_categories(player_cards, shared_cards)
    assert result == {
        "overCardCount": 2,
        "highPairCount": 0,
        "betweenCount": 1,
        "lowPairCount": 0,
        "underCardCount": 2
    }

    player_cards = [treys.Card.new("Jh"), treys.Card.new("6d")]
    shared_cards = [treys.Card.new("As"), treys.Card.new("Kd"), treys.Card.new("7h"), treys.Card.new("6c"), treys.Card.new("2s")]
    result = count_pair_and_high_card_categories(player_cards, shared_cards)
    assert result == {
        "overCardCount": 2,
        "highPairCount": 0,
        "betweenCount": 1,
        "lowPairCount": 1,
        "underCardCount": 1
    }

    player_cards = [treys.Card.new("Jh"), treys.Card.new("Jd")]
    shared_cards = [treys.Card.new("As"), treys.Card.new("Js"), treys.Card.new("Jc"), treys.Card.new("6c"), treys.Card.new("2s")]
    result = count_pair_and_high_card_categories(player_cards, shared_cards)
    assert result == {
        "overCardCount": 1,
        "highPairCount": 2,
        "betweenCount": 0,
        "lowPairCount": 0,
        "underCardCount": 2
    }

    player_cards = [treys.Card.new("Ah"), treys.Card.new("2h")]
    shared_cards = [treys.Card.new("As"), treys.Card.new("Js"), treys.Card.new("Jc"), treys.Card.new("6c"), treys.Card.new("2s")]
    result = count_pair_and_high_card_categories(player_cards, shared_cards)
    assert result == {
        "overCardCount": 0,
        "highPairCount": 1,
        "betweenCount": 3,
        "lowPairCount": 1,
        "underCardCount": 0
    }

def _to_rank(card_str):
    return treys.Card.get_rank_int(treys.Card.new(card_str))

def test_enumerate_pair_and_high_card_outs():
    player_cards = [treys.Card.new("Ah"), treys.Card.new("2h")]
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

    player_cards = [treys.Card.new("Ah"), treys.Card.new("2h")]
    shared_cards = [treys.Card.new("Ks"), treys.Card.new("Js"), treys.Card.new("Jc"), treys.Card.new("6c"), treys.Card.new("3s")]
    result = enumerate_pair_and_high_card_outs(player_cards, shared_cards)
    #This should include every tuple of a dealer's hand that would beat the player.
    assert (treys.Card.new("Ac"), treys.Card.new("Jd")) in result
    assert (treys.Card.new("Ah"), treys.Card.new("Ts")) in result
    remaining_cards = get_remaining_cards(player_cards, shared_cards)
    for card in remaining_cards:
        if card is not treys.Card.new("Kd"):
            assert (treys.Card.new("Kd"), card) in result
    assert len(result) == 497

    player_cards = [treys.Card.new("3h"), treys.Card.new("2h")]
    shared_cards = [treys.Card.new("Ks"), treys.Card.new("Js"), treys.Card.new("Jc"), treys.Card.new("6c"), treys.Card.new("4s")]
    result = enumerate_pair_and_high_card_outs(player_cards, shared_cards)
    #This should include every tuple of a dealer's hand that would beat the player.
    assert (treys.Card.new("Ac"), treys.Card.new("Jd")) in result
    assert (treys.Card.new("Ah"), treys.Card.new("Ts")) in result
    assert len(result) == 1971