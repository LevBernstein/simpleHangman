# Simple Hangman Bot
# Author: Lev Bernstein

HANGMAN = [
    "*******\n*  I  *\n*     *\n*     *\n*     *\n*     *\n*******",
    "*******\n*  I  *\n*  O  *\n*     *\n*     *\n*     *\n*******",
    "*******\n*  I  *\n*  O  *\n*  |  *\n*     *\n*     *\n*******",
    "*******\n*  I  *\n*  O  *\n*  |  *\n*  |  *\n*     *\n*******",
    "*******\n*  I  *\n*  O  *\n* \|  *\n*  |  *\n*     *\n*******",
    "*******\n*  I  *\n*  O  *\n* \|/ *\n*  |  *\n*     *\n*******",
    "*******\n*  I  *\n*  O  *\n* \|/ *\n*  |  *\n* /   *\n*******",
    "*******\n*  I  *\n*  O  *\n* \|/ *\n*  |  *\n* / \ *\n*******",
    "*******\n*  I  *\n*  O  *\n* \|/ *\n*  |  *\n*_/ \ *\n*******",
    "*******\n*  I  *\n*  O  *\n* \|/ *\n*  |  *\n*_/ \_*\n*******" # Dead
]

def setup():
    global order, guesses, words, progress
    order = list("ESIARNTOLCDUPMGHBYFVKWZXQJ-")
    guesses = 0
    words = []
    progress = []
    wordLen = int(input("What is the length of your word?\n"))
    try:
        with open("words.txt", "r") as wordList:
            for line in wordList.read().splitlines():
                if wordLen == len(line):
                    words.append(line.upper())
    except:
        print("Error! Could not read words.txt!")
        return False
    if len(words) < 1:
        print("I have no words of that length in my dictionary. Sorry.")
        return False
    for i in range(wordLen):
        progress.append("_")
    return True

def status():
    print(HANGMAN[guesses])
    result = ""
    for letter in progress:
        result += letter + "  "
    print("Current word status:")
    print(result[:-2])
    result = ""
    for i in range(len(progress)):
        result += str(i+1) + "__"
    print(result[:-2])

def guess():
    global order
    if not "_" in progress:
        print("Yay! I win!")
        return "1"
    if guesses > 8: # arbitrary limit on 8 guesses. Just felt like doing 8.
        print("Oh no! I ran out of guesses! Guess I lose...")
        return "-1"
    searching = True
    while searching:
        if len(order) == 0:
            print("Error! I can't think of any valid words for these letters! Guess I lose...")
            return "-1"
        guess = order[0]
        order.pop(0)
        for word in words:
            if guess in word:
                searching = False
                break
    return guess

def main():
    global progress, words, guesses
    valid = setup()
    if not valid:
        return
    gaming = True
    while gaming:
        status()
        letter = guess()
        if letter == "-1" or letter == "1":
            return
        response = False
        while not response:
            correct = input("My guess is " + letter + "! Was I right? If so, please type yes. If not, please type no.\n").lower()
            if correct != "yes" and correct != "no" and correct != "y" and correct != "n":
                print("Invalid response!")
            else:
                response = True
        if correct.startswith("y"):
            newWords = []
            print("I'm so smart.")
            if progress.count("_") > 1:
                valid = False
                while not valid:
                    valid = True
                    positions = input("Please enter the positions in which this letter appears, starting at 1 on the left, separated by a space.\n").split(" ")
                    for position in positions:
                        if progress[int(position) - 1] != "_":
                            valid = False
                            break
                    if not valid:
                        print("There's already a letter in at least one of the positions you gave!")
                for position in positions:
                    progress[int(position) - 1] = letter
                for word in words:
                    if letter in word:
                        valid = True
                        for i in range (len(progress)):
                            if progress[i] != "_":
                                if progress[i] != word[i]:
                                    valid = False
                                    break
                        if valid:
                            newWords.append(word)
                words = newWords
            else: # if only one blank left, autofill
                for i in range(len(progress)):
                    if progress[i] == "_":
                        progress[i] = letter
        else:
            print("Oops. Well, nobody's perfect.")
            guesses += 1
            newWords = []
            for word in words:
                if letter not in word:
                    newWords.append(word)
            words = newWords
        #print(words) # uncomment this line to see the program narrow down the words with each guess

if __name__ == "__main__":
    main()