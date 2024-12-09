import csv
import random
import pygame
import tkinter as tk
from tkinter import messagebox, simpledialog
import re

pygame.mixer.init()
correctAnswer = pygame.mixer.Sound("y2mate.com - Correct Answer sound effect.wav")
wrong_answer = pygame.mixer.Sound("y2mate.com - Wrong Answer Sound effect.wav")
game_over = pygame.mixer.Sound("y2mate.com - Game Over Sound Effects High Quality.wav")

def play_sounds():
    pygame.mixer.init()
    pygame.mixer.music.load("y2mate.com - Merry Go Round Of Life from Howls Moving Castle  Vitamin String Quartet.mp3")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(loops=-1)

class QuizGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Ultimate Challenge Quiz")
        window_width = 800
        window_height = 400
        self.master.geometry(f"{window_width}x{window_height}")
        self.master.configure(bg="#f0f0f0")

        self.center_window(window_width, window_height)
        self.title_label = tk.Label(master, text="Welcome to Ultimate Challenge Quiz", font=("Arial", 20), bg="#f0f0f0")
        self.title_label.pack(pady=50)

        self.start_button = tk.Button(master, text="Start Quiz",  width=15, height=1,command=self.start_quiz, bg="#4CAF50", fg="white")
        self.start_button.pack(pady=10)

        self.leaderboard_button = tk.Button(master, text="View Leaderboards", command=self.display_leaderboards, bg="#2196F3", fg="white")
        self.leaderboard_button.pack(pady=10)

        self.how_to = tk.Button(master, text="How to play?",  width=15, height=1, command=self.show_detail, bg="#2196F3", fg="white")
        self.how_to.pack(pady=10)

        self.exit_button = tk.Button(master, text="Exit", width=15, height=1,command=master.quit, bg="#f44336", fg="white")
        self.exit_button.pack(pady=10)

        self.questions = []
        self.lives = 3
        self.score = 0
        self.consecutive_correct = 0

    def center_window(self, width, height):
        # Get the screen dimensions
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()

        # Calculate x and y coordinates for the Tkinter window
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)

        # Set the position of the window
        self.master.geometry(f"{width}x{height}+{x}+{y}")

    def start_quiz(self):
        self.player_name = simpledialog.askstring("Input", "Enter your name:")
        if not self.player_name or not re.match("^[A-Za-z0-9 ]+$", self.player_name):
            messagebox.showwarning("Warning", "You need to enter a valid name (no special characters)!")
            return
        if not self.player_name:
            messagebox.showwarning("Warning", "You need to enter your name!")
            return

        self.category_selection()

    def category_selection(self):
        categories = ["Trivia", "Science", "Math", "Literary", "History"]
        self.clear_screen()

        tk.Label(self.master, text="Select a Category", font=("Arial", 16), bg="#f0f0f0").pack(pady=10)
        for category in categories:
            tk.Button(self.master, text=category, width=15, height=2,command=lambda c=category: self.select_category(c),
                      bg="#2196F3", fg="white").pack(pady=5)


    def select_category(self, category):
        self.category = category
        self.difficulty_selection()

    def difficulty_selection(self):
        difficulties = ["Easy", "Normal", "Expert"]
        self.clear_screen()
        tk.Label(self.master, text="Select Difficulty", font=("Arial", 16), bg="#f0f0f0").pack(pady=10)
        for difficulty in difficulties:
            tk.Button(self.master, text=difficulty,width=15, height=2, command=lambda d=difficulty: self.select_difficulty(d),
                      bg="#4CAF50", fg="white").pack(pady=5)


    def select_difficulty(self, difficulty):
        self.difficulty = difficulty
        self.load_questions()
        self.ask_questions()

    def clear_screen(self):
        for widget in self.master.winfo_children():
            widget.destroy()

    def load_questions(self):
        file_name = f"{self.category}{self.difficulty}.csv"  # Assuming the CSV files are named after categories
        self.questions = []
        try:
            with open(file_name, 'r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row['difficulty'].lower() == self.difficulty.lower():
                        self.questions.append((row['question'], row['answer']))
            random.shuffle(self.questions)
        except FileNotFoundError:
            messagebox.showerror("Error", "Questions file not found!")
            return

    def ask_questions(self):
        self.clear_screen()

        self.status_frame = tk.Frame(self.master, bg="#f0f0f0")
        self.status_frame.pack(pady=10)

        self.lives_label = tk.Label(self.status_frame, text=f"Lives: {self.lives}", font=("Arial", 12), bg="#f0f0f0")
        self.lives_label.pack(side=tk.LEFT, padx=10)

        self.score_label = tk.Label(self.status_frame, text=f"Score: {self.score}", font=("Arial", 12), bg="#f0f0f0")
        self.score_label.pack(side=tk.LEFT, padx=10)

        self.question_label = tk.Label(self.master, text="", font=("Arial", 12), bg="#f0f0f0")
        self.question_label.pack(pady=20)

        self.answer_entry = tk.Entry(self.master, font=("Arial", 12))
        self.answer_entry.pack(pady=10)

        self.submit_button = tk.Button(self.master, text="Submit",width=15, height=1, command=self.submit_answer, bg="#4CAF50", fg="white")
        self.submit_button.pack(pady=10)

        self.hint_button = tk.Button(self.master, text="Hint", width=15, height=1,command=self.give_hint, bg="#FFC107", fg="black")
        self.hint_button.pack(pady=5)

        self.exit_button = tk.Button(self.master, text="Back to Main Menu", command=self.back_to_main_menu, bg="#f44336", fg="white")
        self.exit_button.pack(pady=5)

        self.current_question_index = 0
        self.display_question()

    def display_question(self):
        if self.current_question_index < len(self.questions) and self.lives > 0:
            question = self.questions[self.current_question_index]
            self.question_label.config(text=f"Q{self.current_question_index + 1}: {question[0]}")

            # Update lives and score labels
            self.lives_label.config(text=f"Lives: {self.lives}")
            self.score_label.config(text=f"Score: {self.score}")

            self.answer_entry.delete(0, tk.END)  # Clear the entry field
        else:
            self.end_quiz()

    def check_answer(self, user_input, correct_answer):
        if user_input.strip().lower() == 'hint':
            self.lives -= 1
            messagebox.showinfo("Hint", f"Hint: {correct_answer[0]}...")
        elif user_input.strip().lower() == correct_answer.lower():
            messagebox.showinfo("Correct!", "Correct!")
            self.score += 1
            self.consecutive_correct += 1
            if self.consecutive_correct == 3:
                self.lives += 1
                messagebox.showinfo("Extra Life", "You've earned an extra life!")
                self.consecutive_correct = 0
        else:
            messagebox.showinfo("Wrong!", f"Wrong! The answer is: {correct_answer}")
            self.lives -= 1
            self.consecutive_correct = 0

    def submit_answer(self):
        if self.lives > 0:
            user_input = self.answer_entry.get()
            correct_answer = self.questions[self.current_question_index][1]
            self.check_answer(user_input, correct_answer)

            self.current_question_index += 1
            self.display_question()

    def give_hint(self):
        if self.lives > 0:
            correct_answer = self.questions[self.current_question_index][1]
            hint = correct_answer[0] + "..."  # Simple hint: first letter of the answer
            self.lives -= 1  # Deduct a life for using a hint
            messagebox.showinfo("Hint", f"Hint: {hint}\nLives left: {self.lives}")
        else:
            messagebox.showwarning("No Lives Left", "You have no lives left to use a hint.")

    def back_to_main_menu(self):
        # Reset game state variables
        self.lives = 3
        self.score = 0
        self.consecutive_correct = 0
        self.questions = []

        # Clear the screen and show the main menu
        self.clear_screen()
        self.setup_main_menu()

    def setup_main_menu(self):
        self.title_label = tk.Label(self.master, text="Welcome to Ultimate Challenge Quiz", font=("Arial", 20),bg="#f0f0f0")
        self.title_label.pack(pady=50)

        self.start_button = tk.Button(self.master, text="Start Quiz", width=15, height=1, command=self.start_quiz, bg="#4CAF50", fg="white")
        self.start_button.pack(pady=10)

        self.leaderboard_button = tk.Button(self.master, text="View Leaderboards", width=15, height=1, command=self.display_leaderboards,bg="#2196F3", fg="white")
        self.leaderboard_button.pack(pady=10)

        self.exit_button = tk.Button(self.master, text="Exit", width=15, height=1, command=self.master.quit, bg="#f44336", fg="white")
        self.exit_button.pack(pady=10)

    def check_answer(self, user_input, correct_answer):
        if user_input.strip().lower() == 'hint':
            self.lives -= 1
            messagebox.showinfo("Hint", f"Hint: {correct_answer[0]}...")
        elif user_input.strip().lower() == correct_answer.lower():
            pygame.mixer.Sound.play(correctAnswer)
            messagebox.showinfo("Correct!", "Correct!")
            self.score += 1
            self.consecutive_correct += 1
            if self.consecutive_correct == 3:
                self.lives += 1
                messagebox.showinfo("Extra Life", "You've earned an extra life!")
                self.consecutive_correct = 0
        else:
            pygame.mixer.Sound.play(wrong_answer)
            messagebox.showinfo("Wrong!", f"Wrong! The answer is: {correct_answer}")
            self.lives -= 1
            self.consecutive_correct = 0

    def end_quiz(self):
        pygame.mixer.Sound.play(game_over)
        messagebox.showinfo("Game Over", f"Your final score: {self.score - 1}/{len(self.questions)}")
        self.save_results()

    def save_results(self):
        with open('quiz_results.csv', mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([self.player_name, self.difficulty, self.category, self.score-1])

    def display_leaderboards(self):
        try:
            with open('quiz_results.csv', mode='r') as file:
                reader = csv.reader(file)
                leaderboard = f"{'Name':<15}\t{'Difficulty':<25}\t{'Category':<20}\t{'Score':<25}\t"
                leaderboard += "=" * 40
                for row in reader:
                    leaderboard += f"{row[0]:<15}\t{row[1]:<25}\t{row[2]:<20}\t{row[3]:<15}\n"

                messagebox.showinfo("Leaderboards", leaderboard)
        except FileNotFoundError:
            messagebox.showerror("Error", "No leaderboard data found.")

    def show_detail(self):
        how_to_play_message = """
        To start, click on the Start Quiz button and enter your name 
        (only letters and numbers allowed). After that, you'll select a quiz category from options like Trivia, 
        Science, Math, Literary, or History. Once you've picked a category, you'll choose your difficulty level: 
        Easy, Normal, or Expert. The quiz will then begin, displaying questions based on your category and difficulty. 
        Type your answer into the text box and click Submit. Correct answers will earn you points, and answering 
        three consecutive questions correctly will grant you an extra life. Incorrect answers will cost you a life. 
        If you're stuck, you can click the Hint button to reveal the first letter of the correct answer, but this 
        will deduct one of your lives. You start with 3 lives, and if you run out, the game ends. Your score will 
        increase for each correct answer, and you can check the Leaderboards at any time to see how you stack up 
        against others. Good luck, and may the best player win!
        """
        messagebox.showinfo("How to Play", how_to_play_message)
if __name__ == "__main__":
    play_sounds()
    root = tk.Tk()
    game = QuizGame(root)
    root.mainloop()