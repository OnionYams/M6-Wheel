#M6 Wheel of fortune sim

# rules notes: players can buy vowels whenever during their turn, ie don't need to spin first
# players spin for each consonant guess, and CAN spin the same value
# only 19 instead of 24 wheel options, bankrupt, lose turn and 17 values 100 to 900 by 50, no duplicates
# since the wheel is less harsh, there's no money that's immune. ie, you can use money from past round to buy vowels, but
# bankrupts will make the player lose EVERYTHING
# reward for winning round 1 or 2 is 1000 * the round
# turn continues from where it left off, ie player 1 solves round 1, round 2 starts with player 2
# lose your turn if you buy a wrong vowel, otherwise 1 person with bank just buys out everything
#see readme for other rules notes

import random

f = open("words.txt", "r")
wordList = f.read().split()
# globals for tracking multiple games
usedWords = []
gameRound = 1
playTurn = 1
playMoney = [0,0,0]


# bankrupt = 0,  lose turn = 1, left as ints so can do math operation on rest of values more easily
wheelOptions = []
for i in range(2,19):
    wheelOptions.append(i*50)
wheelOptions.append(0)
wheelOptions.append(1)

# run one instance of the game
def round1and2():
    # vars controlling the game
    # generate non used random word from list
    tempWord = wordList[random.randint(0,len(wordList)-1)]
    global usedWords
    while tempWord in usedWords:
        tempWord = wordList[random.randint(0,len(wordList)-1)]
    usedWords.append(tempWord)

    # UNCOMMENT THIS NEXT LINE FOR TESTING
    #print(usedWords)
    # 2 versions for a workaround later
    realWord = remainWord = tempWord
    answer = ""
    for i in range(len(remainWord)):
        answer += "_"
    letters = []
    # global to persist across games
    # some might not have needed to be globals for this but w/e
    global gameRound, playTurn, playMoney, wheelOptions

    #repeat until round ends
    runRound = True
    # game starts
    while (runRound):
        # reset turn
        if playTurn > 3:
            playTurn = 1
        #utility info
        print(F"""----------------------\nIt's round {gameRound}. Player {playTurn}, Choose an option:
1. Spin the Wheel\n2. Buy a Vowel\n3. Guess the Word""")
        print(f"Player 1: ${playMoney[0]}. Player 2: ${playMoney[1]}. Player 3: ${playMoney[2]}.")
        print(answer)
        print(f"Guessed Letters: {letters}")
        #print and check menu
        menuItem = -1
        while menuItem <= 0 or menuItem > 3:
            try: 
                menuItem = int(input(""))
                if menuItem <= 0 or menuItem > 3:
                    print("Not a valid number")
            except: 
                print("Must be an integer menu option")

        if menuItem == 1:
            # check if valid consonants left to guess, could have all consonant but still missing 1 vowel
            numVowels = (letters.count("a") + letters.count("e") + letters.count("i") + letters.count("o") +
                letters.count("u") )
            if len(letters) - numVowels >= 21:
                print("No more consonants left to guess")
                continue
            #spin wheel
            spin = wheelOptions[random.randint(0,len(wheelOptions)-1)]
            if spin == 0:
                print("You went bankrupt. Next player's turn")
                playMoney[playTurn-1] = 0
                playTurn += 1
                continue
            elif spin == 1: 
                print("You lost your turn. Next player's turn")
                playTurn += 1
                continue
            print(f"You spun ${spin}")
            guess = ""
            # nested while to get guesses until 1 is valid
            invalGuess = True
            while (invalGuess):
                guess = str(input("Guess a consonant: ")).lower()
                if not guess.isalpha():
                    print("Please enter a letter")
                elif len(guess) != 1 :
                    print("Please only guess 1 letter at a time")
                elif guess in letters:
                    print("That letter has already been guessed, try another one")
                elif guess == "a" or guess == "e" or guess == "i" or guess == "o" or guess == "u":
                    print("You have to pay for vowels, guess a consonant")
                else:
                    letters += guess
                    invalGuess = False
            #handle valid guess
            if  remainWord.find(guess) == -1:
                print("That letter was not found. Next player's turn")
                playTurn += 1
                continue
            # essentially "moves" letter from a duplicate of the true word to the answer so find can be used for repeated letters  
            # and doesn't only find the first match
            correctLetters = 0 # track how much money to give
            while remainWord.find(guess) != -1:
                answer = answer[:remainWord.find(guess)] + guess + answer[remainWord.find(guess)+len(guess):]
                remainWord = remainWord[:remainWord.find(guess)] + "_" + remainWord[remainWord.find(guess)+len(guess):]
                correctLetters += 1
            #info about money earned
            playMoney[playTurn-1] += spin * correctLetters
            print(f"You got ${spin * correctLetters} for {correctLetters} {guess}'s")   
            # if full word guessed, continue
            if answer == realWord:
                print(f"That's correct. The word was {realWord}. You get ${gameRound*1000}")
                runRound = False
                playMoney[playTurn-1] += gameRound * 1000
                gameRound += 1
                playTurn += 1
        #buy vowel
        elif menuItem == 2:
            if playMoney[playTurn-1] < 250:
                print("You don't have the money to buy a vowel")
                continue
            # can't buy more vowels if none are left
            if (letters.count("a") == 1 and letters.count("e") == 1 and letters.count("i") == 1 and letters.count("o") == 1
                and letters.count("u") == 1 ):
                print("There aren't any more vowels to buy")
                continue
            #copied from 1, guess meaning vowel
            guess = ""
            # nested while to get vowels until 1 is valid
            invalGuess = True
            while (invalGuess):
                guess = str(input("Input a vowel to buy: ")).lower()
                if not guess.isalpha():
                    print("Please enter a letter")
                elif len(guess) != 1 :
                    print("Please only choose 1 vowel at a time")
                elif guess in letters:
                    print("That letter has already been guessed, try another one")
                # changed ors to ands and == to != but really should have just made this the correct condition lol
                elif guess != "a" and guess != "e" and guess != "i" and guess != "o" and guess != "u":
                    print("Please select a vowel")
                else:
                    letters += guess
                    invalGuess = False
            #purchase goes through
            playMoney[playTurn-1] -= 250

            if  remainWord.find(guess) == -1:
                print("That letter was not found. Next player's turn")
                playTurn += 1
            # essentially "moves" letter from a duplicate of the true word to the answer so find can be used for repeated letters  
            # and doesn't only find the first match
            correctLetters = 0 # track how much money to give
            while remainWord.find(guess) != -1:
                answer = answer[:remainWord.find(guess)] + guess + answer[remainWord.find(guess)+len(guess):]
                remainWord = remainWord[:remainWord.find(guess)] + "_" + remainWord[remainWord.find(guess)+len(guess):]
                correctLetters += 1
                
            print(f"You found {correctLetters} {guess}'s")   
            if answer == realWord:
                print(f"That's correct. The word was {realWord}. You get ${gameRound*1000}")
                runRound = False
                playMoney[playTurn-1] += gameRound * 1000
                gameRound += 1
                playTurn += 1
        #guess word    
        elif menuItem == 3:
            guess = str(input("Try to guess the word: ")).lower()
            # thought about only allowing words of correct length but technically players can guess whatever they want
            while not guess.isalpha():
                print("Error. Illegal characters or numbers found. Try again")
                guess = str(input("Try to guess the word: ")).lower()
            # reset round after correct answer
            if guess.lower() == realWord:
                    print(f"That's correct. The word was {realWord}. You get ${gameRound*1000}")
                    runRound = False
                    playMoney[playTurn-1] += gameRound * 1000
                    gameRound += 1
                    playTurn += 1
            else:
                print("That's incorrect. Next player's turn")
                playTurn += 1

def round3():
    #generate word
    tempWord = wordList[random.randint(0,len(wordList)-1)]
    global usedWords
    while tempWord in usedWords:
        tempWord = wordList[random.randint(0,len(wordList)-1)]
    usedWords.append(tempWord)
    # 2 versions for a workaround later
    realWord = remainWord = tempWord
    answer = ""
    for i in range(len(remainWord)):
        answer += "_"
    letters = []
    global gameRound
    
    #if tied, goes to player 1 or first player who's tied
    playNum = 0
    for i in range(3):
        if playMoney[i] == max(playMoney):
            print(f"----------------------\nRound 3: Player {i+1}, you had the most money with ${playMoney[i]}, so you will play")
            print("""R,S,T,L,N and E have been revealed for this puzzle. guess 3 more consonants and 1 vowel, then you 
will have to guess the final puzzle to win $5000""")
            playNum = i+1
            continue
    
    #preadd letters to answer
    letters.append("r")
    letters.append("s")
    letters.append("t")
    letters.append("l")
    letters.append("n")
    letters.append("e")
    # definitely a better way to do this but this reuses what's alreayd written
    guess = "r"
    while remainWord.find(guess) != -1:
                answer = answer[:remainWord.find(guess)] + guess + answer[remainWord.find(guess)+len(guess):]
                remainWord = remainWord[:remainWord.find(guess)] + "_" + remainWord[remainWord.find(guess)+len(guess):]
    guess = "s"
    while remainWord.find(guess) != -1:
                answer = answer[:remainWord.find(guess)] + guess + answer[remainWord.find(guess)+len(guess):]
                remainWord = remainWord[:remainWord.find(guess)] + "_" + remainWord[remainWord.find(guess)+len(guess):]
    guess = "t"
    while remainWord.find(guess) != -1:
                answer = answer[:remainWord.find(guess)] + guess + answer[remainWord.find(guess)+len(guess):]
                remainWord = remainWord[:remainWord.find(guess)] + "_" + remainWord[remainWord.find(guess)+len(guess):]
    guess = "l"
    while remainWord.find(guess) != -1:
                answer = answer[:remainWord.find(guess)] + guess + answer[remainWord.find(guess)+len(guess):]
                remainWord = remainWord[:remainWord.find(guess)] + "_" + remainWord[remainWord.find(guess)+len(guess):]
    guess = "n"
    while remainWord.find(guess) != -1:
                answer = answer[:remainWord.find(guess)] + guess + answer[remainWord.find(guess)+len(guess):]
                remainWord = remainWord[:remainWord.find(guess)] + "_" + remainWord[remainWord.find(guess)+len(guess):]
    guess = "e"
    while remainWord.find(guess) != -1:
                answer = answer[:remainWord.find(guess)] + guess + answer[remainWord.find(guess)+len(guess):]
                remainWord = remainWord[:remainWord.find(guess)] + "_" + remainWord[remainWord.find(guess)+len(guess):]
    
    #get consonants and add them to answer
    for i in range(3):
        print(answer)
        invalGuess = True
        while (invalGuess):
                guess = str(input("Enter a consonant: ")).lower()
                if not guess.isalpha():
                    print("Please enter a letter")
                elif len(guess) != 1 :
                    print("Please only guess 1 letter at a time")
                elif guess in letters:
                    print("That letter has already been guessed, try another one")
                elif guess == "a" or guess == "e" or guess == "i" or guess == "o" or guess == "u":
                    print("You cannot enter vowels at this time, guess a consonant")
                else:
                    letters += guess
                    invalGuess = False
        while remainWord.find(guess) != -1:
                answer = answer[:remainWord.find(guess)] + guess + answer[remainWord.find(guess)+len(guess):]
                remainWord = remainWord[:remainWord.find(guess)] + "_" + remainWord[remainWord.find(guess)+len(guess):] 

    #get vowel 
    invalGuess = True
    while (invalGuess):
                print(answer)
                guess = str(input("Enter a vowel: ")).lower()
                if not guess.isalpha():
                    print("Please enter a letter")
                elif len(guess) != 1 :
                    print("Please only choose 1 vowel at a time")
                elif guess in letters:
                    print("That letter has already been guessed, try another one")
                # changed ors to ands and == to != but really should have just made this the correct condition lol
                elif guess != "a" and guess != "e" and guess != "i" and guess != "o" and guess != "u":
                    print("Please select a vowel")
                else:
                    letters += guess
                    invalGuess = False

            # essentially "moves" letter from a duplicate of the true word to the answer so find can be used for repeated letters  
            # and doesn't only find the first match
    while remainWord.find(guess) != -1:
            answer = answer[:remainWord.find(guess)] + guess + answer[remainWord.find(guess)+len(guess):]
            remainWord = remainWord[:remainWord.find(guess)] + "_" + remainWord[remainWord.find(guess)+len(guess):] 

    print(answer)
    guess = str(input("Try to guess the word: ")).lower()
            # thought about only allowing words of correct length but technically players can guess whatever they want
    while not guess.isalpha():
                print("Error. Illegal characters or numbers found. Try again")
                guess = str(input("Try to guess the word: ")).lower()
    if guess.lower() == realWord:
                print(f"That's correct. The word was {realWord}. You get $5000, Player {playNum}, making your total ${5000 + playMoney[playNum-1]}!")
                gameRound += 1
    else:
                print(f"That's too bad, The word was {realWord}. You lost, but you still got ${playMoney[playNum-1]}!")
                gameRound += 1


print("Welcome to Wheel of Fortune! Please see the Readme for notes on this variation of the game")

# play game rounds
while(gameRound==1 or gameRound==2):
    round1and2()

while(gameRound==3):
    round3()
print("Game over")

f.close()
