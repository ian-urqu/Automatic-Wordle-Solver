import csv
letters = {chr(i): 0 for i in range(ord('a'), ord('z')+1)}

# These letters will represent the dictionary, and their values tell you
# about where they will be found in the word: 0 as default, -1 unknown,
# -2 to -6 (absolute value - 1 = wrong placement) if they are somewhere in the word, -1 if they are not in the word
# at all, and 1-5 is their place in the word for sure.

# letters of significance here for TESTING
letters['p'] = -1
letters['e'] = -1
letters['n'] = -1
letters['i'] = -1
letters['s'] = 5
letters['a'] = 1
letters['b'] = -1
letters['h'] = -1
letters['o'] = -1
letters['r'] = -1
# letters['c'] = 1
# letters['u'] = 2
# letters['l'] = -1
# letters['t'] = -1
# letters['y'] = -1
# letters['z'] = -1
# letters['u'] = -1
# letters['r'] = -4
# letters['f'] = 4
# letters['s'] = -1
# letters['n'] = -2
# letters['a'] = 2
# letters['s'] = -1
# letters['t'] = -5
# letters['y'] = 5

#TODO 

#MAKE THESE DICTIONARIES TO SAVE WHICH SPOTS ARE INCORRECT


# every word possible to guess
AllWords = []
with open('valid-words.csv', 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            word = row[0]
            AllWords.append(word)

# word bank of possible correct answers
WordBank = []
with open('word-bank.csv', 'r') as csvfile:
    csvreader = csv.reader(csvfile)
    for row in csvreader:
        word = row[0]
        WordBank.append(word)

def newWordList(list,letters):
    """
    Returns a new word list to choose the next guess from, depending on
    the letter dictionary.
    """
    wordList = []
    #create dictionary of correct letters
    correct_letters = {}
    for letter in letters:
        if letters[letter] > 0:
            correct_letters.update({letter: letters[letter]})
    print(correct_letters)
    
    #create list of correct letters but incorrect spot
    correct_spot_letters = {}
    for letter in letters:
        if letters[letter] <= -2:
            correct_spot_letters.update({letter: (abs(letters[letter])-2)})
    

    print(correct_spot_letters)
    
    #create dictionary of incorrect letters
    incorrect_letters = []
    for letter in letters:
        if letters[letter] == -1:
            incorrect_letters.append(letter)

    candidates = []
    # if there are more correct_spot_letters than 5, then there are more
    # possible, which should normally be 5 letters (5 letter words only allow that many)
    # by default, this should be false, however for later word decisions, we want to guess
    # a word that may contain any number of these possible letters, which helps narrow down
    # our guess.        
    if len(correct_spot_letters) <= 5:
    
        # Iterate over each word in word list
        for word in list:
            # first find candidates, so loop through every word and mark down the 
            # ones that have every single letter with -2 and less in it

            # create first count, count is increased when a correct letter is in the word
            # if count is equal to the number of correct spot letters, then that word is a candidate!
            matching_letters = [letter for letter in incorrect_letters if letter in word]
            if matching_letters:
                continue
            count1 = 0
            for letter in correct_spot_letters:
                if letter in word and letter != word[correct_spot_letters[letter]]:
                    count1 += 1

                
            if count1 == len(correct_spot_letters):
                candidates.append(word)

        # create second count, this one is increased if correct letter is in correct spot
        # if count is equal to number of correct letters, then that candidate is in in the word list   
        count2 = 0
        for c in candidates:
            count2 = sum(1 for letter in correct_letters if c[correct_letters[letter]-1] == letter)
            if count2 == len(correct_letters.keys()):
                wordList.append(c)
    else:
        for word in list:
            # first find candidates, so loop through every word and mark down the 
            # ones that have every single letter with -2 and less in it

            # create first count, count is increased when a correct letter is in the word
            # if count is equal to the number of correct spot letters, then that word is a candidate!
            matching_letters = [letter for letter in incorrect_letters if letter in word]
            if matching_letters:
                continue
            
            for letter in correct_spot_letters:
                if letter in word and letter != word[correct_spot_letters[letter]]:
                    wordList.append(word)

    return wordList

def generateCommonLetters(list):
    commonly_ordered_alpha = {"e": 0, "i": 0, "s": 0, "a": 0, "r": 0,
                              "n": 0, "t": 0, "0": 0, "l": 0, "c": 0,
                              "u": 0, "d": 0, "p": 0, "m": 0, "g": 0,
                              "h": 0, "b": 0, "y": 0, "f": 0, "v": 0,
                              "k": 0, "k": 0, "w": 0, "z": 0, "x": 0,
                              "o": 0, "j": 0,}
    for word in list:
        for letter in commonly_ordered_alpha:
            if letter in word and letters[letter] == 0:
                commonly_ordered_alpha[letter] = 1

    return commonly_ordered_alpha            


def generateDummyWord(list, letters_dict):
    """
    Returns a separate dictionary of the entire alphabet, but of possible letters to use in
    a new guess
    """
    max_count = 0
    dummy_word = ''


    for word in list:
        count = 0
        repeats = False
        for letter in letters_dict:
            if letters_dict[letter] == 1 and letter in word:
                count += 1
        if count > max_count and len(set(word)) == len(word):  # Check for unique letters
            max_count = count
            dummy_word = word
    
            for l in dummy_word:
                if letters[l] != 0:
                    repeats = True
                    max_count = 0
                    break
        if repeats:
            continue    


    return dummy_word

       


def validWordsFromList(list):
    """
    Returns a list of the words that are possible answers that match the words in the word bank.
    """
    possible_words = []
    for word in list:
        if word in WordBank:
            possible_words.append(word)

    return possible_words        

def dummyWords(dict):
    """
    From a dictionary of letters, find words that contain the most of those letters. This is for a
    next guess so that these letters can be eliminated. Returns a dictionary of dummy words, and these will
    be used to update the stored information about the game to create new guesses.
    """
    possible_words = {}
    pass

def finalGuess(word_list, letter_dict):
    max_count = 0
    final_word = word_list[0]

    for word in word_list:
        count = 0
        for letter in letter_dict:
            if letter_dict[letter] == 1 and letter in word:
                count += 1
        print(f"Word: {word}, Count: {count}, Max Count: {max_count}")  # Debug print
        if count > max_count:
            max_count = count
            final_word = word

    return final_word


#print(newWordList(AllWords, letters))
common_letters = generateCommonLetters(newWordList(AllWords,letters))
print(common_letters)
dummy_words = generateDummyWord(AllWords,generateCommonLetters(newWordList(AllWords, letters)))
print(dummy_words)
valid_words = validWordsFromList(newWordList(AllWords, letters))
print(valid_words)
if len(valid_words) == 1:
    final_guess = (finalGuess(valid_words,common_letters))
    print("Final guess is: " + final_guess)



