
import treys
from river_eval import count_pair_and_high_card_categories

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
