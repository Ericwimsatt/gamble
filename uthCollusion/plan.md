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


###### Pair logic 
Implement enumerate_pair_and_high_card_outs. The out counting should be done similarly to how a player will generally do this at a table.
Start by looking at the counts variable. 
If the player has a pair in their hand, increment highPairCount by 1
Sort the shared cards. 
Start with the highest rank shared card. Evaluate the first remaining_card that matches the rank. if the count of shared+dealer cards of this rank > the players highest count of same rank, or if its == the players highest count of same rank and is a higher rank, then every other remaining card paired with this card will be an out. Remove this card from the remaining_cards, and add this card paired with any other remaining_card to the outs list. 
Else, if player wins even when dealer has a card matching the board, check if dealer wins if the second card in their hand is also the same rank (This might not always be possible if there's only 1 card of this rank in remaining_cards). Evaluate if this hand beats the player hand. The initial card can be removed from the remaining_cards after this
Repeat this process for all cards that pair with the shared_cards.
Then, after evaluating cards that match the board, if the player has a pair, only consider cases where the dealer has a pair in their hand. If player does not have a pair, evaluate cases where dealer has 1 card higher than the players highest card. 
The key is we're evaluating the dealer's best card, going through every possible second card in the dealers hand, and then removing the best card from the remaining_cards for the rest of the operation. We can take some shortcuts based on knowledge of pairs along the way