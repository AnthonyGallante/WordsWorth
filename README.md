# WordsWorth

A Wordle-like word puzzle game with resource management mechanics, built using Python and Tkinter.

## Game Overview

WordsWorth combines the popular word-guessing mechanics of Wordle with a resource management system. Players need to guess a 5-letter word while managing their coin economy.

### Game Rules

1. **Objective**: Guess the hidden 5-letter word within 6 attempts.
2. **Resource Management**: Players start with 10 coins (💰) and spend them to guess letters.
   - Non-vowel letters cost 1 coin each
   - Vowels (A, E, I, O, U) cost 3 coins each
   - **Letters that have been guessed previously become FREE in subsequent guesses**
3. **Earnings**: When a guess is submitted, players earn:
   - 2 coins for each letter in the correct position (green)
   - 1 coin for each letter that's in the word but in the wrong position (yellow)
4. **Strategy**: Players can forfeit a turn to gain 7 coins, sacrificing one of their 6 attempts.
5. **Game End**: The game ends when the player correctly guesses the word or uses all 6 attempts.

## Project Structure

The project is organized as follows:

```
WordsWorth/
├── main.py             # Entry point for the application
├── gui.py              # Tkinter GUI implementation
├── wordle_game.py      # Game logic module
├── word_list.py        # Word dictionary management
├── resources/          # Directory containing word lists
│   └── five_letter_words.txt   # List of 5-letter words (created at runtime)
└── README.md           # This documentation file
```

## Dependencies

- Python 3.6 or higher
- Tkinter (included in standard Python installation)

## Installation

1. Clone the repository or download the source code:
   ```
   git clone https://github.com/yourusername/WordsWorth.git
   cd WordsWorth
   ```

2. Run the game:
   ```
   python main.py
   ```

## How to Play

1. **Starting the Game**: Run `main.py` to launch the game interface.
2. **Making a Guess**: 
   - Type letters using your keyboard or click the on-screen keyboard.
   - The cost of your current word is displayed below the game board.
   - Previously guessed letters will be FREE (shown at the top of the screen).
   - Click "SUBMIT" or press Enter to submit your guess.
3. **Reading Results**:
   - Green tiles: Letters in the correct position
   - Yellow tiles: Letters in the word but wrong position
   - Gray tiles: Letters not in the word
4. **Managing Resources**:
   - Keep an eye on your coin count (displayed at the top)
   - Remember that previously guessed letters are free to use again
   - Click "FORFEIT TURN" to gain 7 coins and skip a turn
5. **Starting Over**: Click "NEW GAME" to start a fresh game with a new word.

## Customizing the Game

You can modify the game's parameters by editing the following files:

- **wordle_game.py**: Change starting coins, costs, or rewards
- **word_list.py**: Modify word length or word source
- **gui.py**: Customize colors, fonts, or layout

## Technical Implementation

### Word Selection
The game uses a dictionary of 1,000 five-letter English words. It automatically downloads a word list from the internet or generates one if the download fails. The list is filtered to include only 5-letter words and stored in the `resources` directory.

### Game Logic
The core game logic is separated from the GUI, making it easier to modify or extend. The `WordleGame` class in `wordle_game.py` handles:
- Word selection and validation
- Guess evaluation
- Resource management
- Game state tracking

### User Interface
The GUI is built with Tkinter and features:
- A larger window (550x800) to ensure all letters fit properly
- A game board with spacious colored tiles
- An on-screen keyboard with standardized key sizes in QWERTY layout
- Coin emoji (💰) displays instead of the word "coin" 
- Properly spaced elements to prevent overlapping
- Action buttons of equal size for a more uniform appearance
- A display of previously guessed (free) letters for easier tracking

## Credits

Developed by [Your Name/Organization]

Inspired by:
- Wordle (by Josh Wardle)
- Modern word games with resource management mechanics 