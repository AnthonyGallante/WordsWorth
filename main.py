#!/usr/bin/env python3
"""
WordsWorth - A Wordle-like game with resource management
"""

import tkinter as tk
from gui import WordsWorthGUI

def main():
    """Main function to start the game"""
    root = tk.Tk()
    app = WordsWorthGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main() 