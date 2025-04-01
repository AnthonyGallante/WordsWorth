from word_list import WordList

class WordleGame:
    def __init__(self):
        self.word_list = WordList()
        self.max_attempts = 6
        self.current_attempt = 0
        self.target_word = ""
        self.guesses = []
        self.results = []
        self.coins = 10
        self.vowels = set(['A', 'E', 'I', 'O', 'U'])
        self.game_over = False
        self.won = False
        self.coin_emoji = "💰"
        
    def start_new_game(self):
        """Start a new game with a random target word"""
        self.target_word = self.word_list.get_random_word()
        self.current_attempt = 0
        self.guesses = []
        self.results = []
        self.coins = 12
        self.game_over = False
        self.won = False
        return self.target_word
    
    def get_letter_cost(self, letter):
        """Calculate the cost of a letter"""
        letter = letter.upper()
        return 3 if letter in self.vowels else 1
    
    def calculate_word_cost(self, word):
        """Calculate the cost to guess a word"""
        total_cost = 0
        for letter in word.upper():
            total_cost += self.get_letter_cost(letter)
        return total_cost
    
    def can_afford_word(self, word):
        """Check if player has enough coins for the word"""
        return self.coins >= self.calculate_word_cost(word)
    
    def submit_guess(self, guess):
        """Submit a guess and process the result"""
        if self.game_over:
            return False, "Game is over. Start a new game."
        
        if self.current_attempt >= self.max_attempts:
            self.game_over = True
            return False, "You've used all your attempts."
        
        guess = guess.upper()
        
        # Validate the guess
        if len(guess) != 5:
            return False, "Guess must be 5 letters."
        
        if not guess.isalpha():
            return False, "Guess must contain only letters."
        
        if not self.word_list.is_valid_word(guess):
            return False, "Not in word list."
        
        # Check if player can afford this word
        word_cost = self.calculate_word_cost(guess)
        if self.coins < word_cost:
            return False, f"Not enough coins. Need {word_cost}, have {self.coins}."
        
        # Process the guess
        self.coins -= word_cost
        self.current_attempt += 1
        self.guesses.append(guess)
        
        # Calculate the result and coins earned
        result = self.evaluate_guess(guess)
        self.results.append(result)
        
        coins_earned = 0
        for status in result:
            if status == 2:  # Right letter, right position (green)
                coins_earned += 2
            elif status == 1:  # Right letter, wrong position (yellow)
                coins_earned += 1
        
        self.coins += coins_earned
        
        # Check if the player won
        if guess == self.target_word:
            self.won = True
            self.game_over = True
            return True, f"Correct! You won with {self.current_attempt} attempts and {self.coins} coins left."
        
        # Check if the player lost
        if self.current_attempt >= self.max_attempts:
            self.game_over = True
            return True, f"Game over. The word was {self.target_word}. You have {self.coins} coins left."
        
        return True, f"Earned {coins_earned} coins. {self.coins} coins remaining."
    
    def forfeit_turn(self):
        """Forfeit a turn to gain coins"""
        if self.game_over:
            return False, "Game is over. Start a new game."
        
        if self.current_attempt >= self.max_attempts:
            self.game_over = True
            return False, "You've used all your attempts."
        
        # Add coins and consume a turn
        self.coins += 7
        self.current_attempt += 1
        self.guesses.append("")
        self.results.append([])
        
        # Check if the player lost due to using all attempts
        if self.current_attempt >= self.max_attempts:
            self.game_over = True
            return True, f"Game over. The word was {self.target_word}. You have {self.coins} coins left."
        
        return True, f"Turn forfeited. Gained 7 coins. Now have {self.coins} coins. {self.max_attempts - self.current_attempt} attempts remaining."
    
    def evaluate_guess(self, guess):
        """Evaluate a guess against the target word
        Returns a list of status codes:
        0 = letter not in word (gray)
        1 = letter in word but wrong position (yellow)
        2 = letter in correct position (green)
        """
        target = self.target_word
        result = [0] * 5
        
        # Create copies to track which letters have been matched
        target_letters = list(target)
        guess_letters = list(guess)
        
        # First pass: check for exact matches (green)
        for i in range(5):
            if guess_letters[i] == target_letters[i]:
                result[i] = 2
                # Mark these letters as used
                target_letters[i] = "*"
                guess_letters[i] = "#"
        
        # Second pass: check for letters in wrong position (yellow)
        for i in range(5):
            if guess_letters[i] != "#":  # Skip already matched letters
                if guess_letters[i] in target_letters:
                    result[i] = 1
                    # Mark this letter as used
                    target_letters[target_letters.index(guess_letters[i])] = "*"
        
        return result
    
    def get_game_state(self):
        """Return the current state of the game"""
        return {
            "current_attempt": self.current_attempt,
            "max_attempts": self.max_attempts,
            "coins": self.coins,
            "guesses": self.guesses,
            "results": self.results,
            "game_over": self.game_over,
            "won": self.won
        } 