#M6 Wheel of fortune sim

#rules notes: players can buy vowels whenever during their turn, ie don't need to spin first
# players spin for each consonant guess, and CAN spin the same value
# only 19 instead of 24 wheel options, bankrupt, lose turn and 17 values 100 to 900 by 50
# player 1 starts each round

import random

f = open("words.txt", "r")
wordList = f.read().split()
# globals for tracking multiple games
usedWords = []
gameRound = 0
playTurn = 1
playMoney = [0,0,0]


# bankrupt = 0,  lose turn = 1, left as ints so can do math operation on rest of values more easily
wheelOptions = []
for i in range(2,20):
    wheelOptions.append(i*50)
wheelOptions.append(0)
wheelOptions.append(1)
print(wheelOptions)


# run one instance of the game
def runGame():
    # vars controlling the game
    numGuesses = 7
    # generate non used random word from list
    tempWord = wordList[random.randint(0,len(wordList)-1)]
    global usedWords
    while tempWord in usedWords:
        tempWord = wordList[random.randint(0,len(wordList)-1)]
    usedWords += tempWord
    # 2 versions for a workaround later
    realWord = remainWord = tempWord
    answer = ""
    for i in range(len(remainWord)):
        answer += "_"
    letters = []
    # global to persist across games
    global wins, losses

    # game starts
    while (numGuesses > 0):
        guess = str(input("----------------------\nGuess a letter: "))
        # validate input
        if not guess.isalpha():
            print("Must enter a letter or word")
            continue
        if guess in letters:
            print("Already guessed that")
            continue
        guess = guess.lower()
        # only allow guessing 1 letter or entire word, any other length guess is invalid
        if len(guess) == 1:
            letters += guess
        elif len(guess) != len(realWord):
            print("Please only guess one letter at a time or the entire word")
            continue
        else: 
            if guess == realWord:
                print("----------------------\nYou win. The word was " + realWord)
                wins += 1
                break
            # if tried to guess entire word but failed, handle loss
            numGuesses -= 1
            print("Incorrect, remaining guesses: " + str(numGuesses))
            print(answer)
            print(f"Wins: {wins}  Losses: {losses} Guesses: {letters}")
            if numGuesses == 0:
                print("----------------------\nYou lose. the word was " + realWord)
                losses += 1
            continue
        # handle if guess not found in word 
        if remainWord.find(guess) == -1:
            numGuesses -= 1
            print("Incorrect, remaining guesses: " + str(numGuesses))
            print(answer)
            print(f"Wins: {wins}  Losses: {losses} Guesses: {letters}")
            if numGuesses == 0:
                print("----------------------\nYou lose. the word was " + realWord)
                losses += 1
            continue
        # essentially "moves" letter from a duplicate of the true word to the answer so find can be used for repeated letters  
        # and doesn't only find the first match
        while remainWord.find(guess) != -1:
            answer = answer[:remainWord.find(guess)] + guess + answer[remainWord.find(guess)+len(guess):]
            remainWord = remainWord[:remainWord.find(guess)] + "_" + remainWord[remainWord.find(guess)+len(guess):]
        print(answer)
        print(f"Wins: {wins}  Losses: {losses} Guesses: {letters}")
        if answer == realWord:
            print("----------------------\nYou win. The word was " + realWord)
            wins += 1
            break

# play game again if desired
while(playGame):
    runGame()
    print(f"Wins: {wins}  Losses: {losses}")
    if input("Enter 'Y' to play again or any other input to exit the game: ").upper() == "Y":
        continue
    else:
        playGame = False
        print("Goodbye") 
        
f.close()
