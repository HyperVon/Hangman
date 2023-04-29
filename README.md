# Hangman Game

A simple, text-based Hangman game with a graphical user interface (GUI) created using Python and tkinter. The game selects a random word from a list of words and the player needs to guess the word by choosing one letter at a time. The player has a limited number of tries to guess the word. The game keeps track of the player's score and best score.

## Requirements

- Python 3.6+
- tkinter
- requests

## Installation

1. Clone the repository or download the source code.
2. Install the required packages (if not already installed):
    pip install -r requirements.txt
3. Run the `main.py` script to start the game: python main.py

## Game Instructions

1. The game starts with a random word, represented by underscores.
2. Select a letter by clicking on the letter buttons. The selected letter will be disabled after you click on it.
3. If the letter is in the word, it will be revealed in the correct position(s).
4. If the letter is not in the word, a part of the hangman character will be drawn, and the number of tries remaining will be decreased.
5. The game ends when:
   - The player guesses the word correctly.
   - The player runs out of tries.
6. To play again, click the "Play Again" button.

## Sample Game Play Video
https://www.youtube.com/watch?v=O4R3yaCzSOE

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.



