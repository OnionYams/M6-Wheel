# M6-Wheel

Simulation of Wheel of fortune with some alternate rules for 3 players(can be played by 1)

rules notes: players can buy vowels whenever during their turn, ie don't need to spin first
players spin for each consonant guess, and CAN spin the same value
only 19 instead of 24 wheel options, bankrupt, lose turn and 17 values 100 to 900 by 50, no duplicates
since the wheel is less harsh, there's no money that's immune. ie, you can use money from past round to buy vowels, but
bankrupts will make the player lose EVERYTHING
reward for winning round 1 or 2 is 1000 * the round
turn continues from where it left off, ie player 1 solves round 1, round 2 starts with player 2
lose your turn if you buy a wrong vowel, otherwise 1 person with bank just buys out everything
goes by player order for who plays round 3 if multiple people are tied
no time limit for final guess because that's a bit anticlimactic to lose to a clock