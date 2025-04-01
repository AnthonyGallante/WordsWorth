import tkinter as tk
from tkinter import messagebox, font
import string
from wordle_game import WordleGame

class WordsWorthGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("WordsWorth")
        self.root.resizable(False, False)
        self.root.configure(bg="#121213")
        
        # Reduced window width from 600 to 550, increased height from 800 to 850
        self.root.geometry("550x850")
        
        # Coin emoji
        self.coin_emoji = "💰"
        
        # Color scheme (similar to Wordle)
        self.colors = {
            "bg": "#121213",               # Background color
            "key_bg": "#818384",           # Key background
            "correct": "#538d4e",          # Green (correct position)
            "present": "#b59f3b",          # Yellow (in word, wrong position)
            "absent": "#3a3a3c",           # Grey (not in word)
            "key_text": "white",           # Key text color
            "text": "#d7dadc",             # General text color
            "border": "#3a3a3c",           # Border color
            "title": "#d7dadc",            # Title color
            "forfeit": "#f5793a",          # Forfeit button color
            "submit": "#538d4e"            # Submit button color
        }
        
        # Fonts
        self.title_font = font.Font(family="Helvetica", size=28, weight="bold")
        self.letter_font = font.Font(family="Helvetica", size=24, weight="bold")
        self.key_font = font.Font(family="Helvetica", size=12, weight="bold")  # Reduced from 14 to 12
        self.info_font = font.Font(family="Helvetica", size=14)
        self.button_font = font.Font(family="Helvetica", size=12, weight="bold")
        
        # Game logic
        self.game = WordleGame()
        self.game.start_new_game()
        
        # Current guess
        self.current_word = ""
        self.current_row = 0
        
        # Set to track guessed letters (they will be free in subsequent guesses)
        self.guessed_letters = set()
        
        # Create widgets
        self._create_widgets()
        
        # Add key press event
        self.root.bind("<Key>", self._handle_key_press)
    
    def _create_widgets(self):
        # Main container to organize elements vertically
        main_container = tk.Frame(self.root, bg=self.colors["bg"])
        main_container.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)  # Reduced padding from 20 to 15
        
        # Title frame
        title_frame = tk.Frame(main_container, bg=self.colors["bg"])
        title_frame.pack(pady=(10, 0))
        
        title_label = tk.Label(title_frame, text="WordsWorth", font=self.title_font, 
                               fg=self.colors["title"], bg=self.colors["bg"])
        title_label.pack()
        
        # Info frame (coins display)
        self.info_frame = tk.Frame(main_container, bg=self.colors["bg"])
        self.info_frame.pack(pady=(10, 20))
        
        self.coins_label = tk.Label(self.info_frame, 
                                    text=f"{self.coin_emoji} {self.game.coins}", 
                                    font=self.info_font, fg=self.colors["text"], 
                                    bg=self.colors["bg"])
        self.coins_label.pack()
        
        # Guessed letters display
        self.guessed_letters_frame = tk.Frame(main_container, bg=self.colors["bg"])
        self.guessed_letters_frame.pack(pady=(0, 10))
        
        self.guessed_letters_label = tk.Label(self.guessed_letters_frame, 
                                    text="Free letters: None", 
                                    font=self.info_font, fg=self.colors["text"], 
                                    bg=self.colors["bg"])
        self.guessed_letters_label.pack()
        
        # Game board frame
        board_frame = tk.Frame(main_container, bg=self.colors["bg"], padx=10, pady=10)
        board_frame.pack()
        
        # Create grid of letter tiles (6 rows, 5 columns)
        self.tiles = []
        for i in range(6):
            row_tiles = []
            row_frame = tk.Frame(board_frame, bg=self.colors["bg"])
            row_frame.pack(pady=5)
            
            for j in range(5):
                # Make tiles larger
                tile = tk.Label(row_frame, width=3, height=1, font=self.letter_font,
                               bg=self.colors["bg"], fg=self.colors["text"], 
                               relief="solid", bd=2, borderwidth=2)
                tile.configure(highlightbackground=self.colors["border"], highlightthickness=2)
                tile.pack(side=tk.LEFT, padx=5)
                row_tiles.append(tile)
            
            self.tiles.append(row_tiles)
        
        # Word cost display label - moved it above action buttons
        cost_frame = tk.Frame(main_container, bg=self.colors["bg"], pady=10)
        cost_frame.pack()
        
        self.cost_label = tk.Label(cost_frame, text=f"Word Cost: 0 {self.coin_emoji}", 
                                  font=self.info_font, fg=self.colors["text"], bg=self.colors["bg"])
        self.cost_label.pack()
        
        # Action buttons frame
        action_frame = tk.Frame(main_container, bg=self.colors["bg"], pady=10)
        action_frame.pack()
        
        # Standardize button size with width and height
        button_width = 10
        button_height = 2
        
        self.submit_button = tk.Button(action_frame, text="SUBMIT", font=self.button_font,
                                      bg=self.colors["submit"], fg="white", 
                                      width=button_width, height=button_height,
                                      command=self._submit_guess)
        self.submit_button.pack(side=tk.LEFT, padx=10)
        
        self.forfeit_button = tk.Button(action_frame, text=f"FORFEIT TURN\n+7 {self.coin_emoji}", 
                                       font=self.button_font,
                                       bg=self.colors["forfeit"], fg="white", 
                                       width=button_width + 2, height=button_height,
                                       command=self._forfeit_turn)
        self.forfeit_button.pack(side=tk.LEFT, padx=5)
        
        self.new_game_button = tk.Button(action_frame, text="NEW GAME", font=self.button_font,
                                        bg=self.colors["key_bg"], fg="white", 
                                        width=button_width, height=button_height,
                                        command=self._start_new_game)
        self.new_game_button.pack(side=tk.LEFT, padx=10)
        
        # Keyboard frame - repositioned and resized
        keyboard_frame = tk.Frame(main_container, bg=self.colors["bg"], pady=15)  # Reduced from 20 to 15
        keyboard_frame.pack(pady=(10, 0))
        
        # Create keyboard with three rows - smaller key size
        self.key_buttons = {}
        key_width = 3  # Reduced from 4 to 3
        key_height = 1  # Reduced from 2 to 1
        key_padx = 1    # Reduced padding between keys
        
        # Row 1: Q to P
        row1_frame = tk.Frame(keyboard_frame, bg=self.colors["bg"])
        row1_frame.pack(pady=1)  # Reduced from 2 to 1
        
        for letter in "QWERTYUIOP":
            btn = tk.Button(row1_frame, text=letter, font=self.key_font, 
                          width=key_width, height=key_height, 
                          bg=self.colors["key_bg"], fg=self.colors["key_text"],
                          command=lambda l=letter: self._add_letter(l))
            btn.pack(side=tk.LEFT, padx=key_padx)
            self.key_buttons[letter] = btn
        
        # Row 2: A to L
        row2_frame = tk.Frame(keyboard_frame, bg=self.colors["bg"])
        row2_frame.pack(pady=1)  # Reduced from 2 to 1
        
        # Add half-size spacer for offset (QWERTY layout)
        tk.Label(row2_frame, width=1, bg=self.colors["bg"]).pack(side=tk.LEFT)  # Reduced from 2 to 1
        
        for letter in "ASDFGHJKL":
            btn = tk.Button(row2_frame, text=letter, font=self.key_font, 
                          width=key_width, height=key_height,
                          bg=self.colors["key_bg"], fg=self.colors["key_text"],
                          command=lambda l=letter: self._add_letter(l))
            btn.pack(side=tk.LEFT, padx=key_padx)
            self.key_buttons[letter] = btn
        
        # Row 3: Z to M, Backspace
        row3_frame = tk.Frame(keyboard_frame, bg=self.colors["bg"])
        row3_frame.pack(pady=1)  # Reduced from 2 to 1
        
        # Add spacer for offset (QWERTY layout)
        tk.Label(row3_frame, width=2, bg=self.colors["bg"]).pack(side=tk.LEFT)  # Added wider spacer for proper QWERTY alignment
        
        for letter in "ZXCVBNM":
            btn = tk.Button(row3_frame, text=letter, font=self.key_font, 
                          width=key_width, height=key_height,
                          bg=self.colors["key_bg"], fg=self.colors["key_text"],
                          command=lambda l=letter: self._add_letter(l))
            btn.pack(side=tk.LEFT, padx=key_padx)
            self.key_buttons[letter] = btn
        
        # Backspace button - place a bit after the M key
        tk.Label(row3_frame, width=1, bg=self.colors["bg"]).pack(side=tk.LEFT)  # Spacer
        backspace_btn = tk.Button(row3_frame, text="←", font=self.key_font, 
                                width=key_width, height=key_height,
                                bg=self.colors["key_bg"], fg=self.colors["key_text"],
                                command=self._remove_letter)
        backspace_btn.pack(side=tk.LEFT, padx=key_padx)
        
        # Update cost display
        self._update_cost_display()
    
    def _handle_key_press(self, event):
        """Handle keyboard input"""
        key = event.char.upper()
        
        if event.keysym == "BackSpace":
            self._remove_letter()
        elif event.keysym == "Return":
            self._submit_guess()
        elif key in string.ascii_uppercase and len(key) == 1:
            self._add_letter(key)
    
    def _add_letter(self, letter):
        """Add a letter to the current guess"""
        if self.game.game_over:
            return
        
        if len(self.current_word) < 5:
            self.current_word += letter
            # Update the tile
            col = len(self.current_word) - 1
            self.tiles[self.current_row][col].config(text=letter)
            
            # Update the cost display
            self._update_cost_display()
    
    def _remove_letter(self):
        """Remove the last letter from the current guess"""
        if self.game.game_over:
            return
        
        if len(self.current_word) > 0:
            # Clear the tile
            col = len(self.current_word) - 1
            self.tiles[self.current_row][col].config(text="")
            
            # Remove the letter
            self.current_word = self.current_word[:-1]
            
            # Update the cost display
            self._update_cost_display()
    
    def _calculate_word_cost(self, word):
        """Calculate the cost of a word, with already guessed letters being free"""
        total_cost = 0
        for letter in word.upper():
            # Skip cost for already guessed letters
            if letter not in self.guessed_letters:
                total_cost += self.game.get_letter_cost(letter)
        return total_cost
    
    def _update_cost_display(self):
        """Update the cost display based on the current word"""
        if self.current_word:
            # Use our custom cost calculation that factors in free letters
            cost = self._calculate_word_cost(self.current_word)
            affordable = self.game.coins >= cost
            
            self.cost_label.config(text=f"Word Cost: {cost} {self.coin_emoji}", 
                                  fg="green" if affordable else "red")
        else:
            self.cost_label.config(text=f"Word Cost: 0 {self.coin_emoji}", fg=self.colors["text"])
    
    def _update_coins_display(self):
        """Update the coins display"""
        self.coins_label.config(text=f"{self.coin_emoji} {self.game.coins}")
    
    def _update_guessed_letters_display(self):
        """Update the display of guessed (free) letters"""
        if self.guessed_letters:
            sorted_letters = sorted(list(self.guessed_letters))
            self.guessed_letters_label.config(text=f"Free letters: {' '.join(sorted_letters)}")
        else:
            self.guessed_letters_label.config(text="Free letters: None")
    
    def _submit_guess(self):
        """Submit the current guess"""
        if self.game.game_over:
            self._show_message("Game Over", "The game is already over. Start a new game.")
            return
        
        if len(self.current_word) != 5:
            self._show_message("Invalid Word", "Your guess must be 5 letters long.")
            return
        
        # Calculate the cost with free letters
        custom_cost = self._calculate_word_cost(self.current_word)
        
        # Check if player can afford this word with the custom cost
        if self.game.coins < custom_cost:
            self._show_message("Error", f"Not enough coins. Need {custom_cost}, have {self.game.coins}.")
            return
        
        # Validate the word exists in dictionary
        guess = self.current_word.upper()
        if not self.game.word_list.is_valid_word(guess):
            self._show_message("Error", "Not in word list.")
            return
        
        # Pay the coins (custom amount)
        self.game.coins -= custom_cost
        
        # Add all letters in the guess to the set of guessed letters
        for letter in guess:
            self.guessed_letters.add(letter)
        
        # Update displays
        self._update_guessed_letters_display()
        
        # Process the guess
        self.game.current_attempt += 1
        self.game.guesses.append(guess)
        
        # Calculate the result and coins earned
        result = self.game.evaluate_guess(guess)
        self.game.results.append(result)
        
        coins_earned = 0
        for status in result:
            if status == 2:  # Right letter, right position (green)
                coins_earned += 2
            elif status == 1:  # Right letter, wrong position (yellow)
                coins_earned += 1
        
        self.game.coins += coins_earned
        
        # Update the tiles with colors based on the results
        self._color_row()
        
        # Update keyboard colors
        self._update_keyboard()
        
        # Move to the next row
        self.current_row += 1
        self.current_word = ""
        
        # Update displays
        self._update_coins_display()
        self._update_cost_display()
        
        # Check if the player won
        if guess == self.game.target_word:
            self.game.won = True
            self.game.game_over = True
            self._show_message("Congratulations!", 
                            f"Correct! You won with {self.game.current_attempt} attempts and {self.game.coins} {self.coin_emoji} left.")
            return
        
        # Check if the player lost
        if self.game.current_attempt >= self.game.max_attempts:
            self.game.game_over = True
            self._show_message("Game Over", 
                            f"Game over. The word was {self.game.target_word}. You have {self.game.coins} {self.coin_emoji} left.")
            return
        
        # Game continues
        self._show_message("Good guess!", f"Earned {coins_earned} {self.coin_emoji}. {self.game.coins} {self.coin_emoji} remaining.")
    
    def _forfeit_turn(self):
        """Forfeit the current turn for coins"""
        if self.game.game_over:
            self._show_message("Game Over", "The game is already over. Start a new game.")
            return
        
        # Confirm the forfeit
        if not messagebox.askyesno("Forfeit Turn", 
                                  f"Are you sure you want to forfeit this turn and gain 7 {self.coin_emoji}?"):
            return
        
        # Clear the current word
        self.current_word = ""
        for i in range(5):
            self.tiles[self.current_row][i].config(text="")
        
        # Submit the forfeit
        success, message = self.game.forfeit_turn()
        
        if success:
            # Move to the next row
            self.current_row += 1
            
            # Update displays
            self._update_coins_display()
            self._update_cost_display()
            
            # Show message
            self._show_message("Turn Forfeited", message.replace("coins", self.coin_emoji))
            
            # Show game over message if needed
            if self.game.game_over:
                self._show_message("Game Over", message.replace("coins", self.coin_emoji))
        else:
            # Show error message
            self._show_message("Error", message.replace("coins", self.coin_emoji))
    
    def _color_row(self):
        """Color the current row based on the game results"""
        results = self.game.results[self.current_row]
        guess = self.game.guesses[self.current_row]
        
        for i in range(5):
            color = self.colors["bg"]
            if results[i] == 2:
                color = self.colors["correct"]
            elif results[i] == 1:
                color = self.colors["present"]
            elif results[i] == 0:
                color = self.colors["absent"]
            
            self.tiles[self.current_row][i].config(bg=color)
    
    def _update_keyboard(self):
        """Update the keyboard colors based on all results so far"""
        # Track the best status for each letter
        letter_status = {}
        
        # Go through all guesses and results
        for i, (guess, result) in enumerate(zip(self.game.guesses, self.game.results)):
            for j, letter in enumerate(guess):
                # Only consider actual letters (not empty strings from forfeits)
                if letter:
                    # Keep the best status for each letter (2 > 1 > 0)
                    current_status = result[j]
                    if letter not in letter_status or current_status > letter_status[letter]:
                        letter_status[letter] = current_status
        
        # Update the keyboard colors
        for letter, status in letter_status.items():
            if letter in self.key_buttons:
                if status == 2:
                    self.key_buttons[letter].config(bg=self.colors["correct"])
                elif status == 1:
                    self.key_buttons[letter].config(bg=self.colors["present"])
                elif status == 0:
                    self.key_buttons[letter].config(bg=self.colors["absent"])
    
    def _start_new_game(self):
        """Start a new game"""
        self.game.start_new_game()
        
        # Reset the UI
        self.current_word = ""
        self.current_row = 0
        
        # Reset guessed letters
        self.guessed_letters = set()
        self._update_guessed_letters_display()
        
        # Clear the tiles
        for i in range(6):
            for j in range(5):
                self.tiles[i][j].config(text="", bg=self.colors["bg"])
        
        # Reset the keyboard
        for letter, button in self.key_buttons.items():
            button.config(bg=self.colors["key_bg"])
        
        # Update displays
        self._update_coins_display()
        self._update_cost_display()
        
        # Show message
        self._show_message("New Game", "A new game has started. Good luck!")
    
    def _show_message(self, title, message):
        """Show a message box"""
        messagebox.showinfo(title, message)

def main():
    root = tk.Tk()
    app = WordsWorthGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main() 