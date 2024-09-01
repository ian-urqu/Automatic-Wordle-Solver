import pyautogui
import time
import random
import csv
from pynput import keyboard, mouse
import WordleBot as w

# Constants for colors in dark mode
COLOR_GREY = (58, 58, 60)
COLOR_YELLOW = (181, 159, 59)
COLOR_GREEN = (83, 141, 78)

# Offsets based on the relative positions of the cells
CELL_WIDTH = 62  # Approximate width of a cell
CELL_HEIGHT = 62  # Approximate height of a cell

first_cell_coords = None

def on_click(x, y, button, pressed):
    global first_cell_coords
    if pressed:
        first_cell_coords = (x, y)
        return False

def get_grid_positions():
    x_start, y_start = first_cell_coords

    # Generate positions for the grid
    grid = []
    for row in range(6):
        current_row = []
        for col in range(5):
            x = x_start + col * (CELL_WIDTH + 9)
            y = y_start + row * (CELL_HEIGHT + 9)
            current_row.append((x, y))
        grid.append(current_row)
    return grid

def type_word(word):
    pyautogui.typewrite(word)
    pyautogui.press('enter')
    words_entered.append(word)

def check_colors(word, row):
    i = 0
    colors = []
    for coord in row:
        pixel_color = pyautogui.pixel(coord[0], coord[1])
        colors.append(pixel_color)
        # grey, incorrect
        if pixel_color == COLOR_GREY:
            letters[word[i]] = -1
        # yellow, incorrect spot but in word
        elif pixel_color == COLOR_YELLOW:
            letters[word[i]] = -2 - i
        # green
        elif pixel_color == COLOR_GREEN:
            letters[word[i]] = i + 1
        i += 1
    return colors

def determine_next_word():
    common_letters = w.generateCommonLetters(w.newWordList(AllWords, letters))
    dummy_words = w.generateDummyWord(AllWords, w.generateCommonLetters(w.newWordList(AllWords, letters)))
    valid_words = w.validWordsFromList(w.newWordList(AllWords, letters))
    if len(valid_words) == 1:
        final_guess = (w.finalGuess(valid_words, common_letters))
        return final_guess
    if len(words_entered) >= 3:
        return random.choice(valid_words)
    if len(valid_words) <= 6 - len(words_entered):
        return random.choice(valid_words)
    return dummy_words

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

def on_press(key):
    try:
        if key.char == '`':
            listener.stop()
    except AttributeError:
        pass

print("Please click on the first cell of the Wordle grid.")
with mouse.Listener(on_click=on_click) as listener:
    listener.join()

print("Press ` to begin")
with keyboard.Listener(on_press=on_press) as listener:
    listener.join()

grid = get_grid_positions()

type_word("heart")
time.sleep(2)
count = 0
while count < len(grid):
    colors = check_colors(words_entered[count], grid[count])
    print(f"Word entered: {words_entered[count]}, Colors detected: {colors}")
    print(words_entered)
    
    # Check if miniscreen has popped up
    # Adjust this part if the location or color is different on macOS or other setups
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
    
    count += 1
    print("Determining next word...")
    time.sleep(4)