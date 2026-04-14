## Tried
Generating win probabilities based on known dead cards

-didn't work because optimal strategy is affected by the ability to make other adjustments later

## Strategy-Checking Cases

Want to be able to factor in dead cards to an optimal strategy

Enumerating every possible combination isn't possible because there's too many scenarios and I only have 100gb open on this computer.

### Memory reducing strats
#### WinCon Counting
Count paths to winning (high card, pair, higher pair, trips, higher trips, straight, flush, straight flush, quads)
Maintain different counts for different conditions
High/Pairs reduction will sum to deck_size
flush/straight reduction will be represented some other way.
##### High/Pairs Reduction
Core assumption is I can model many hands to be similar like the following
- Player has a higher card and lower card
- Every other card is over, highPair, between, lowPair, or under
- All of these cards behave similarly. (ie, if I have Jh, 5d, optimal play changes exactly the same way if there's a Qs, Ks, or As in the flop)  Therefore I can count the remaining number of these cards and then use them interchangeably.

##### Flushes/Straights Counter
For each stage, count number of cards left for a flush on most-shown suit. (some complexity at flop, may need to track multiple numbers; P(PlayerFlush) == suitCount + P(5-suitCount appearing in remaining shard cards))


Straights, open-ended, gutshot, double-gutshot odds can be counted 

- will need to consider dealer having same flush as player and higher card (for straights and flush)

#### Suit reduction
Players highest card is always a heart
Players second card is always a heart or diamond
Shared cards that are a spade or club will always evaluate the same way

Use probability math/outs counting where possible instead of simulations

## Workflow
Preflop: max(EV 4x, EV (PostFlop))

PostFlop = max(EV 2x bet, EV River)


EV River = max(-2, if dealer qualify(3*P))
