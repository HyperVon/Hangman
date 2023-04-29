import os
import random
import tkinter as tk

import requests


class HangmanGame:
    """Handles the game logic for Hangman."""

    def __init__(self):
        self.words = self.load_words()
        self.best_score = 0
        self.reset_game()

    def load_words(self):
        words_file = 'words_alpha.txt'

        if not os.path.exists(words_file):
            url = 'https://github.com/dwyl/english-words/raw/master/words_alpha.txt'
            response = requests.get(url)

            with open(words_file, 'wb') as file:
                file.write(response.content)

        with open(words_file, 'r') as file:
            words = [word.strip().lower() for word in file.readlines()]
        return words

    def reset_game(self):
        self.word = random.choice(self.words)
        self.word_completion = ' '.join('_' * len(self.word))
        self.guessed_letters = []
        self.tries = 6
        self.score = 0

    def submit_guess(self, guess):
        if guess in self.guessed_letters:
            return
        elif guess not in self.word:
            self.tries -= 1
        else:
            word_as_list = list(self.word_completion.split(' '))
            indices = [i for i, letter in enumerate(self.word) if letter == guess]
            for index in indices:
                word_as_list[index] = guess
            self.word_completion = ' '.join(word_as_list)
            self.score += 1

        self.guessed_letters.append(guess)


class HangmanUI:
    """Creates the Hangman game UI using tkinter."""

    def __init__(self, master, game):
        self.master = master
        self.game = game
        master.title('Hangman')

        master.configure(bg='#2d2d2d')
        self.create_widgets()
        self.update_labels()

    def select_letter(self, letter):
        if letter in self.game.guessed_letters:
            return

        self.letter_buttons[letter].config(state=tk.DISABLED)
        self.submit_guess(letter)

    def create_widgets(self):
        self.title_label = tk.Label(self.master, text="Let's play Hangman!", font=('Helvetica', 24), bg='#2d2d2d',
                                    fg='#f1c40f')
        self.title_label.pack(pady=20)

        # Create the canvas for drawing the hangman character
        self.canvas = tk.Canvas(self.master, width=300, height=200, bg='#2d2d2d', highlightthickness=0)
        self.canvas.pack(pady=(0, 20))

        self.display_label = tk.Label(self.master, font=('Helvetica', 18), bg='#2d2d2d', fg='#ecf0f1')
        self.display_label.pack()

        self.score_label = tk.Label(self.master, font=('Helvetica', 14), bg='#2d2d2d', fg='#bdc3c7')
        self.score_label.pack(pady=10)

        self.tries_label = tk.Label(self.master, font=('Helvetica', 14), bg='#2d2d2d', fg='#bdc3c7')
        self.tries_label.pack(pady=10)

        self.chosen_letters_label = tk.Label(self.master, font=('Helvetica', 14), bg='#2d2d2d', fg='#bdc3c7')
        self.chosen_letters_label.pack(pady=10)

        self.keyboard_frame = tk.Frame(self.master, bg='#2d2d2d')
        self.keyboard_frame.pack()

        self.letter_buttons = {}
        letters = 'abcdefghijklmnopqrstuvwxyz'
        for i, letter in enumerate(letters):
            button = tk.Button(self.keyboard_frame, text=letter.upper(), command=lambda l=letter: self.select_letter(l),
                               font=('Helvetica', 12), bg='#34495e', fg='#ecf0f1', state=tk.NORMAL)
            button.grid(row=i // 13, column=i % 13, padx=5, pady=5)
            self.letter_buttons[letter] = button

        button_frame = tk.Frame(self.master, bg='#2d2d2d')
        button_frame.pack()

        self.play_again_button = tk.Button(button_frame, text='Play Again', command=self.play_again, state=tk.DISABLED,
                                           font=('Helvetica', 12), bg='#34495e', fg='#ecf0f1')
        self.play_again_button.pack(side=tk.LEFT, pady=10)

        self.result_label = tk.Label(self.master, text='', font=('Helvetica', 14), bg='#2d2d2d', fg='#f1c40f',
                                     wraplength=550)
        self.result_label.pack(pady=10)

    def update_labels(self):
        self.display_label.config(text=self.game.word_completion)
        self.score_label.config(text=f'Score: {self.game.score} | Best Score: {self.game.best_score}')
        self.tries_label.config(text=f'Tries remaining: {self.game.tries}')
        self.chosen_letters_label.config(text=f'Chosen letters: {", ".join(self.game.guessed_letters)}')

        # Update the hangman character drawing
        self.canvas.delete("all")
        self.draw_hangman()

    def draw_hangman(self):
        tries = self.game.tries
        hangman_color = '#f1c40f'  # Change the hangman color to make it more visible

        # Draw gallows
        self.canvas.create_line(50, 180, 250, 180, fill=hangman_color)
        self.canvas.create_line(150, 180, 150, 50, fill=hangman_color)
        self.canvas.create_line(150, 50, 100, 50, fill=hangman_color)
        self.canvas.create_line(100, 50, 100, 70, fill=hangman_color)

        # Draw head
        if tries < 6:
            self.canvas.create_oval(75, 70, 125, 120, outline=hangman_color)

        # Draw body
        if tries < 5:
            self.canvas.create_line(100, 120, 100, 150, fill=hangman_color)

        # Draw left arm
        if tries < 4:
            self.canvas.create_line(100, 130, 80, 120, fill=hangman_color)

        # Draw right arm
        if tries < 3:
            self.canvas.create_line(100, 130, 120, 120, fill=hangman_color)

        # Draw left leg
        if tries < 2:
            self.canvas.create_line(100, 150, 80, 170, fill=hangman_color)

        # Draw right leg
        if tries < 1:
            self.canvas.create_line(100, 150, 120, 170, fill=hangman_color)

    def submit_guess(self, letter):
        if self.game.tries <= 0:
            self.result_label.config(text=f'Sorry, you ran out of tries. The word was {self.game.word}')
            self.play_again_button.config(state=tk.NORMAL)
            return

        guess = letter  # Use the letter passed to the method

        if len(guess) == 1 and guess.isalpha():
            if guess in self.game.guessed_letters:
                self.result_label.config(text=f'You already guessed the letter {guess}')
            elif guess not in self.game.word:
                self.result_label.config(text=f'{guess} is not in the word.')
                self.game.tries -= 1
                self.game.guessed_letters.append(guess)
                self.update_labels()
            else:
                self.result_label.config(text=f'Good job, {guess} is in the word!')
                self.game.guessed_letters.append(guess)
                self.update_labels()
                word_as_list = list(self.game.word_completion.split(' '))
                indices = [i for i, letter in enumerate(self.game.word) if letter == guess]
                for index in indices:
                    word_as_list[index] = guess
                self.game.word_completion = ' '.join(word_as_list)
                self.display_label.config(text=self.game.word_completion)

                self.game.score += 1
                self.score_label.config(text=f'Score: {self.game.score} | Best Score: {self.game.best_score}')

            if self.game.tries == 0:
                self.result_label.config(text=f'Sorry, you ran out of tries. The word was {self.game.word}')
                self.play_again_button.config(state=tk.NORMAL)
            elif '_' not in self.game.word_completion:
                self.result_label.config(text='Congratulations, you guessed the word! You win!')
                self.play_again_button.config(state=tk.NORMAL)
                if self.game.score > self.game.best_score:
                    self.game.best_score = self.game.score
                    self.score_label.config(text=f'Score: {self.game.score} | Best Score: {self.game.best_score}')

    def play_again(self):
        self.game.reset_game()
        self.update_labels()
        self.result_label.config(text='')
        self.play_again_button.config(state=tk.DISABLED)

        # Re-enable all the letter buttons
        for btn in self.letter_buttons.values():
            btn.config(state=tk.NORMAL)


if __name__ == '__main__':
    root = tk.Tk()
    root.minsize(600, 675)  # Increased height to 675

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    window_width = 600
    window_height = 675  # Increased height to 675

    x = (screen_width // 2) - (window_width // 2)
    y = (screen_height // 2) - (window_height // 2)

    root.geometry(f"{window_width}x{window_height}+{x}+{y}")

    game = HangmanGame()
    hangman_gui = HangmanUI(root, game)
    root.mainloop()
