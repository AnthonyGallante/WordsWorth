import random
import os
import urllib.request

class WordList:
    def __init__(self):
        self.words = []
        self.word_length = 5
        self.resources_dir = "resources"
        self.word_file = os.path.join(self.resources_dir, "five_letter_words.txt")
        self._load_words()
    
    def _load_words(self):
        """Load the word list from file or download it if not available"""
        # Create resources directory if it doesn't exist
        if not os.path.exists(self.resources_dir):
            os.makedirs(self.resources_dir)
        
        # If word file doesn't exist, download it
        if not os.path.exists(self.word_file):
            self._download_word_list()
        
        # Load words from file
        with open(self.word_file, 'r') as f:
            self.words = [word.strip().upper() for word in f.readlines() 
                          if len(word.strip()) == self.word_length]
        
        # Make sure we have enough words
        if len(self.words) < 1000:
            raise ValueError(f"Not enough {self.word_length}-letter words found. Only {len(self.words)} available.")
    
    def _download_word_list(self):
        """Download a list of English words"""
        word_list_url = "https://www.mit.edu/~ecprice/wordlist.10000"
        print(f"Downloading word list from {word_list_url}...")
        
        try:
            urllib.request.urlretrieve(word_list_url, "resources/temp_wordlist.txt")
            
            # Filter to get only 5-letter words
            with open("resources/temp_wordlist.txt", 'r') as infile, \
                 open(self.word_file, 'w') as outfile:
                for line in infile:
                    word = line.strip()
                    if len(word) == self.word_length and word.isalpha():
                        outfile.write(word + '\n')
            
            # Remove temp file
            os.remove("resources/temp_wordlist.txt")
        except Exception as e:
            print(f"Error downloading word list: {e}")
            # Fallback: Create a smaller list of common 5-letter words
            self._create_fallback_word_list()
    
    def _create_fallback_word_list(self):
        """Create a fallback word list if download fails"""
        common_words = [
            "ABOUT", "ABOVE", "ACTOR", "ACUTE", "ADAPT", "ADMIT", "ADOPT", "ADORE",
            "ADULT", "AFTER", "AGAIN", "AGENT", "AGREE", "AHEAD", "ALARM", "ALBUM",
            "ALERT", "ALIKE", "ALIVE", "ALLOW", "ALONG", "ALTER", "AMONG", "ANGER",
            "ANGLE", "ANGRY", "ANKLE", "APART", "APPLE", "APPLY", "ARENA", "ARGUE",
            "ARISE", "ARMOR", "ARRAY", "ARROW", "ASSET", "AVOID", "AWARD", "AWARE",
            "BACON", "BADGE", "BADLY", "BAKER", "BASES", "BASIC", "BASIS", "BEACH",
            "BEARD", "BEAST", "BEGIN", "BEING", "BELOW", "BENCH", "BERRY", "BIRTH",
            "BLACK", "BLADE", "BLAME", "BLANK", "BLAST", "BLAZE", "BLEED", "BLEND",
            "BLESS", "BLIND", "BLOCK", "BLOOD", "BLUFF", "BOARD", "BOAST", "BONUS",
            "BOOST", "BOOTH", "BORNE", "BOOTS", "BOTCH", "BOUND", "BRACE", "BRAIN",
            "BRAKE", "BRAND", "BRAVE", "BREAD", "BREAK", "BREED", "BRICK", "BRIDE",
            "BRIEF", "BRING", "BRISK", "BROAD", "BROOK", "BROWN", "BRUSH", "BUILD",
            "BUILT", "BURST", "CABIN", "CABLE", "CAMEL", "CANAL", "CANDY", "CANON",
            "CARGO", "CARRY", "CARVE", "CATCH", "CAUSE", "CEASE", "CHAIN", "CHAIR",
            "CHALK", "CHARM", "CHART", "CHASE", "CHEAP", "CHECK", "CHEEK", "CHEER",
            "CHEST", "CHIEF", "CHILD", "CHILL", "CHINA", "CHOIR", "CHOKE", "CHORD",
            "CIVIL", "CLAIM", "CLASS", "CLEAN", "CLEAR", "CLERK", "CLICK", "CLIFF",
            "CLIMB", "CLOCK", "CLOSE", "CLOTH", "CLOUD", "CLOWN", "COAST", "COLOR",
            "COMIC", "COUNT", "COURT", "COVER", "CRACK", "CRAFT", "CRANE", "CRASH",
            "CRATE", "CRAZY", "CREAM", "CREED", "CREEK", "CREST", "CRIME", "CRISP",
            "CROSS", "CROWD", "CROWN", "CRUDE", "CRUEL", "CRUSH", "CUBIC", "CURVE"
        ]
        
        # Add more words to reach at least 1000
        generated_words = common_words.copy()
        while len(generated_words) < 1000:
            # Generate variations of existing words
            for word in common_words:
                for i in range(5):
                    new_word = list(word)
                    new_word[i] = chr(random.randint(65, 90))  # Random uppercase letter
                    new_word = "".join(new_word)
                    if new_word not in generated_words:
                        generated_words.append(new_word)
                        if len(generated_words) >= 1000:
                            break
                if len(generated_words) >= 1000:
                    break
        
        # Write to file
        with open(self.word_file, 'w') as f:
            for word in generated_words:
                f.write(word + '\n')
    
    def get_random_word(self):
        """Return a random word from the list"""
        return random.choice(self.words)
    
    def is_valid_word(self, word):
        """Check if a word is in the list"""
        return word.upper() in self.words 