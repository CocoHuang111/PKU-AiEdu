- Source: https://ocw.mit.edu/courses/15-s50-how-to-win-at-texas-holdem-poker-january-iap-2016/pages/assignments/
- source_format: html
- capture_date: 2026-10-03
- license: https://creativecommons.org/licenses/by-nc-sa/4.0/

---
## Assignments

### Homework

#### Problem Set 1

1. In Jennifer Tilly’s hand, she has Jd Jc, and the board is Ts Jh 7c Ks Kc. List all hands that actually beat her (you don’t have to list suits, just cards).
2. In Texas Hold’em, getting dealt two Aces (“pocket Aces”) is the best possible starting hand you can hope for. What is the probability of getting dealt this hand?
3. You are in the Button position (ie. you are the dealer) and it’s folded to you. You are trying to exploit the two players in the Small Blind and Big Blind positions, who are way too tight. You know their strategy is to only call any raise with AA (pocket Aces), and fold everything else. The effective stack size is 20BB. Roughly speaking, what should your strategy be in this situation? By strategy, I mean a description of what to do with each potential hand you could have, eg. “raise with QQ,KK,AA and fold everything else”.
4. After the flop, assuming you will see the turn and river, what is the probability of being dealt at least one of 6 cards, without any of 9 other cards appearing? Construct a situation in which two players go all-in on the flop, and the probability of one player winning is approximately this calculation.

Question 4 is taken from Eric Beren’s poker homework at Jane Street Capital.

› *Problem Set 1 Solutions (click to reveal / hide)*

1. KK, KJ, KT, and K7 (any suits)
2. 4/52 is the probability of getting the first ace; 3/51 is the probability of getting the second ace after getting the first ace. Multiply those together to get 1/221 or approximately 0.45%.
3. Intuitively, the best strategy is to raise and attempt to “steal” the blinds with any 2 cards, since the blinds are only putting up resistance with AA, which occurs with a very small probability (calculated in Question 2). However, if they do put up resistance, then we should only continue on flops where we can beat AA, since we know they have AA.
4. At this point in the hand, 7 cards (the 2 cards in each player’s hand, and the 3 flop cards) have been exposed. Out of the 45 cards remaining in the deck, 6 are “good”, 9 are “bad”, and 30 are “neutral”. We are interested in the probability of hitting at least one good card without hitting any bad cards. This can occur if we hit two good cards, or one good card and one neutral card. The probability of hitting two good cards is 6/45*5/44=1/66. The probability of hitting a good card and a neutral card is 2*(6/45*30/44)=3/55. Add these fractions to get 13/66. To construct an example, think of where the numbers 9 or 6 could come from. The 9 “bad” cards could correspond to our opponent having 4 to a flush, and needing 1 of the remaining 9 from the suit. The 6 “good” cards could correspond to one of 6 outs to hit an open-ended straight draw (after subtracting the 2 outs which would complete a flush). A concrete example is: Us: 9c 8c Opponents: Kh Ks Board: Th 7h 2h

#### Problem Set 2

Jen is dealt a random card from a deck with the cards 1,2,…,10. Bill is dealt a random card from a separate deck with the cards 1,2,…,10. Both players are forced to ante $50 into the pot at the start of the hand.

The betting works as follows: only Jen has the option to either Bet $100 or Check. If she checks, then showdown happens immediately and the player with the higher card wins the pot (in the case of a tie, the pot goes to Bill). If she bets, then Bill can either Call or Fold. If Bill Calls, then he also wagers an additional $100 and showdown occurs (now for a larger pot of $300). If Bill Folds, then Jen collects the pot of $100 without showdown.

For each Bill that Jen is playing against, outline her most profitable exploitative strategy. Circle the hands that she should Bet $100 with, and also calculate how much she expects to profit per game using this strategy.

Example: vs. Bill Cosby who calls every card, we only want to “value-bet”. The best strategy is to bet with cards 6’s or better (it actually doesn’t matter whether we bet a 6). The amount we make per game is: half the time, we get dealt 6+, in which case both players wager $150 (since we will bet and he will call) and we will win 70% of the time (we will win 50% of the time if we have a 6, and 90% of the time if we have a 10, so this averages out to 70%); the other half, we get dealt 1-5, in which case both players wager $50 (since we will check) and we will win 20% of the time. The total EV is:

.5(.7*(+150)+.3*(-150))+.5(.2*(+50)+.8*(-50)) = 15

1. Bill Gates: very tight, he will only call with a 10+. 1 2 3 4 5 6 7 8 9 10
2. Bill Nye: pretty loose; he will call with 4+. 1 2 3 4 5 6 7 8 9 10
3. Bill Clinton: pretty tight; he will call with 8+. 1 2 3 4 5 6 7 8 9 10
4. **(bonus)** Bill Chen: he will call with the optimal strategy. Namely, he will call with a range of hands that minimizes how much you expect to win per game. This could be a randomized strategy, eg. “Always call 8+, and call a 7 60% of the time.” Outline what his optimal strategy is, and circle the hands you would bet against this strategy. 1 2 3 4 5 6 7 8 9 10 **(corollary to bonus)** If Jen Shahade (who plays the optimal strategy for Jen vs. Bill’s optimal strategy) plays vs. Bill Chen, who is expected to win? The player who gets to bet (Jen) or the player who wins ties (Bill)?

› *Problem Set 2 Solutions (click to reveal / hide)*

1. bluff 8- or 9-; EV is +31/game
2. value-bet 8+; EV is +$4/game
3. bluff 4- or 5-; EV is +$6/game
4. Bill’s optimal strategy is to call with the top x% of hands, where x can be any real number in [0.45,0.5]. (If x=0.45, then his strategy is to call 7+, and call a 6 50% of the time.) If he does this, Jen’s optimal strategy is to always bluff a 1, never bluff a 2, and always value-bet 9+. Bill actually wins when both players play optimally, profiting $1 per game.
