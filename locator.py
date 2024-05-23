from pyautogui import *
import pyautogui
import time
import keyboard
import random
import win32api, win32con
import csv

import WordleBot as w

#ON DARK MODE RGB COLORS:
# GREY: (58, 58, 60)
# YELLOW: (181, 159, 59)
# GREEN: (83, 141, 78)

#LOCATIONS of PRESSES on 2560x1440 screen at 100% zoom
# Columns:
# 1: 1145
# 2: 1210
# 3: 1280
# 4: 1350
# 5: 1415
# FOR OFFICIAL NYT WEBSITE
# Rows:
# 1: 440
# 2: 510
# 3: 575
# 4: 645
# 5: 705
# 6: 775

# #FOR ARCHIVE
# # Rows:
y1 = 560
y2 = 630
y3 = 690
y4 = 765
y5 = 825
y6 = 895

x1 = 1145
x2 = 1210
x3 = 1280
x4 = 1350
x5 = 1415

# y1 = 440
# y2 = 510
# y3 = 575
# y4 = 645
# y5 = 705
# y6 = 775

first_row = [
    (x1, y1),
    (x2, y1),
    (x3, y1),
    (x4, y1),
    (x5, y1)
]

second_row = [
    (x1, y2),
    (x2, y2),
    (x3, y2),
    (x4, y2),
    (x5, y2)
]

third_row = [
    (x1, y3),
    (x2, y3),
    (x3, y3),
    (x4, y3),
    (x5, y3)
]

fourth_row = [
    (x1, y4),
    (x2, y4),
    (x3, y4),
    (x4, y4),
    (x5, y4)
]

fifth_row = [
    (x1, y5),
    (x2, y5),
    (x3, y5),
    (x4, y5),
    (x5, y5)
]

sixth_row = [
    (x1, y5),
    (x2, y5),
    (x3, y5),
    (x4, y5),
    (x5, y5)
]

grid = []
grid.append(first_row)
grid.append(second_row)
grid.append(third_row)
grid.append(fourth_row)
grid.append(fifth_row)
grid.append(sixth_row)

letters = {chr(i): 0 for i in range(ord('a'), ord('z')+1)}
words_entered = []
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



#TODO 2 write to calculate where from the screen based on first input
# possibly use locate on screen?


#to type a word
def type_word(word):
    pyautogui.typewrite(word)
    pyautogui.press('enter')
    words_entered.append(word)

def check_colors(word, row):
    i = 0
    for coord in row:
        pixel_color = pyautogui.pixel(coord[0], coord[1])
        # grey, incorrect
        if pixel_color == (58, 58, 60):
            letters[word[i]] = -1
        # yellow, incorrect spot but in word
        elif pixel_color == (181, 159, 59):
            letters[word[i]] = -2 - i
        # green
        elif pixel_color == (83, 141, 78):
            letters[word[i]] = i + 1
        i = i + 1

def determine_next_word():
    common_letters = w.generateCommonLetters(w.newWordList(AllWords,letters))
    dummy_words = w.generateDummyWord(AllWords,w.generateCommonLetters(w.newWordList(AllWords, letters)))
    valid_words = w.validWordsFromList(w.newWordList(AllWords, letters))
    if len(valid_words) == 1:
        final_guess = (w.finalGuess(valid_words,common_letters))
        return final_guess
    if len(words_entered) >= 3:
        return random.choice(valid_words)
    if len(valid_words) <= 6 - len(words_entered):
        return random.choice(valid_words)
    return dummy_words



print("Press ` to begin")
keyboard.wait('`')

type_word("heart")
time.sleep(2)
count = 0
while count < len(grid):
    
    check_colors(words_entered[count], grid[count])
    
    # Check if miniscreen has popped up
    # FOR ARCHIVE
    pixel_color = pyautogui.pixel(1480, 943)
    # grey, incorrect
    if pixel_color == (77, 129, 72):
        break
    #if all green letters, break
    all_green = all(letters[letter] == i + 1 for i, letter in enumerate(words_entered[count]))
    
    if all_green:
        print("Completed run.")
        break

    try:
        next_word = determine_next_word()
    except IndexError:
        print("Failed word.") 
        break
    print("Next word: " + next_word)
    type_word(next_word)
    
    
    count = count + 1
    print("Determining next word...")
    time.sleep(4)
    


