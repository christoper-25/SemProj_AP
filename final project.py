import csv
import random
import pygame
import cowsay
from colorama import Fore, Style
pygame.mixer.init()
correct_answer = pygame.mixer.Sound("correct-83487.mp3")
wrong_answer = pygame.mixer.Sound("y2mate.com - Wrong Answer Sound effect.mp3")
game_over = pygame.mixer.Sound("y2mate.com - Game Over Sound Effects High Quality.mp3")

def play_sounds():
    pygame.mixer.init()
    pygame.mixer.music.load("y2mate.com - Merry Go Round Of Life from Howls Moving Castle  Vitamin String Quartet.mp3")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(loops=-1)

def print_title():
    title = f"{Fore.BLUE}-----🅆🄴🄻🄲🄾🄼🄴 🅃🄾 🅄🄻🅃🄸🄼🄰🅃🄴 🄲🄷🄰🄻🄻🄴🄽🄶🄴 🅀🅄🄸🅉-----{Style.RESET_ALL}"
    width = 89
    centered_title = title.center(width)
    print("+------------------------------------------------------------------------------------------------------+")
    print(f"| {centered_title} |")
    print(f"| {Fore.LIGHTGREEN_EX} Test Your Knowledge and Unleash Your Inner Genius!                                                  {Style.RESET_ALL}|")
    print("+------------------------------------------------------------------------------------------------------+")

def display_category_options():
    print(f"Choose a {Fore.GREEN}CATEGORY{Style.RESET_ALL}:")
    categories = [
        f"{Fore.CYAN}1. Trivia Test{Style.RESET_ALL}",
        f"{Fore.CYAN}2. Science Test{Style.RESET_ALL}",
        f"{Fore.CYAN}3. Math Test{Style.RESET_ALL}",
        f"{Fore.CYAN}4. Literary Test{Style.RESET_ALL}",
        f"{Fore.CYAN}5. History Test{Style.RESET_ALL}",
        f"{Fore.CYAN}6. Display Leaderboards{Style.RESET_ALL}",
        f"{Fore.LIGHTRED_EX}7. Exit{Style.RESET_ALL}"

    ]
    for category in categories:
        print(category)
    print("=" * 50)

def display_difficulty_options():
    print("Choose a difficulty level:")
    difficulties = [
        f"{Fore.GREEN}1. Easy{Style.RESET_ALL}",
        f"{Fore.BLUE}2. Normal{Style.RESET_ALL}",
        f"{Fore.RED}3. Expert{Style.RESET_ALL}",
        f"{Fore.BLUE}4. Back{Style.RESET_ALL}"

    ]
    for difficulty in difficulties:
        print(difficulty)
    print("=" * 50)

class MgaTanong:
    def __init__(self, questions,):
        self.questions = questions
        self.lives = 3
        self.score = 0
        self.consecutive_correct = 0  # Counter for consecutive correct answers
        random.shuffle(questions)

    def start_quiz(self):
        print(f"{Fore.RED}CAUTION:  {Style.RESET_ALL}{Fore.LIGHTGREEN_EX}Using a hint will decrease your lives by 1.{Style.RESET_ALL}")

        for index, question in enumerate(self.questions, start=1):
            if self.lives > 0:  # Check if the player has lives left
                print(f"{Fore.GREEN}You have {self.lives} lives remaining.{Style.RESET_ALL}")  # Show lives before asking the question
                self.ask_question(index, question)
                if self.lives == 0:  # Check if lives have reached zero
                    game_over.play()
                    print(f"{Fore.RED}Game Over! You have run out of lives.{Style.RESET_ALL}")
                    break  # Exit the loop if lives are zero
                    game_over.play()
        print(f"Your final score: {self.score}/{len(self.questions)}")
        return self.score

    def ask_question(self, index, question):
        cowsay.cow(f"{Fore.RED}Question {index}{Style.RESET_ALL}: {Fore.BLUE}{question[0]}{Style.RESET_ALL}")

        hint_used = False  # Initialize hint_used before the loop

        while True:
            user_input = input("Enter your answer (or type 'hint' for a hint): ")

            if user_input.strip().lower() == 'hint' and not hint_used:
                hint_used = True
                self.lives -= 1  # Decrease lives by 1 when hint is used
                print(f"{Fore.YELLOW}Hint: {question[1][0]}...{Style.RESET_ALL}")
            elif user_input.strip().lower() == question[1].lower():
                correct_answer.play()
                cowsay.tux(f"{Fore.BLUE}Correct!{Style.RESET_ALL}")
                self.score += 1
                self.consecutive_correct += 1  # Increment consecutive correct answers
                if self.consecutive_correct == 3:
                    self.lives += 1  # Grant an extra life
                    print(f"{Fore.LIGHTGREEN_EX}Congratulations! You've earned an extra life!{Style.RESET_ALL}")
                    self.consecutive_correct = 0  # Reset the counter after earning an extra life
                break
            else:
                wrong_answer.play()
                self.lives -= 1  # Decrease lives by 1 for wrong answer
                cowsay.tux(f"{Fore.RED}Wrong!{Style.RESET_ALL} The answer is: {Fore.BLUE}{question[1]}{Style.RESET_ALL}")
                self.consecutive_correct = 0  # Reset the counter on incorrect answer
                break

        hint_status = "Used" if hint_used else "Not Used"

        print(f"Your current score: {self.score}/{len(self.questions)}| Lives left: {self.lives} | Hint status: {hint_status}\n")
def display_leaderboards():
    print(f"{Fore.YELLOW}--- Leaderboards ---{Style.RESET_ALL}")
    try:
        with open('quiz_results.csv', mode='r') as file:
            reader = csv.reader(file)
            print(f"{'Name':<20} {'Difficulty':<15} {'Category':<20}{'Score':<15}")
            print("=" * 62)
            for row in reader:
                print(f"{row[0]:<20}  {row[1]:<15} {row[2]:<20} {row[3]:<5}")
    except FileNotFoundError:
        print(f"{Fore.RED}No leaderboard data found.{Style.RESET_ALL}")



def save_results(pangalan, difficulty, file_name, score):
    with open('quiz_results.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([pangalan, difficulty, file_name, score])


def main():
    print_title()
    play_sounds()
    while True:
        pangalan = input("Enter your name first before we proceed: ").strip()
        if pangalan:  # Check if the input is not empty
            break
        else:
            print("You need to enter your name!")

    print(f"Welcome {pangalan} to UCQ!!")
    ENTER = f"{Fore.BLUE}ENTER{Style.RESET_ALL}"
    input(f"Press {ENTER} to reveal the category...")

    display_category_options()

    choice = input("Please select an option (1-7): ")

    if choice == '6':
        display_leaderboards()
        return

    if choice == '7':
        print("Exiting the game.!")
        pygame.quit()
        return

    display_difficulty_options()

    difficulty_choice = input("Please select a difficulty level (1-3): ")

    if choice == '1':
        if difficulty_choice == '1':
            difficulty = "easy"
            file_name = "Trivia.csv"
        elif difficulty_choice == '2':
            difficulty = "normal"
            file_name = "TriviaNormal.csv"
        elif difficulty_choice == '3':
            difficulty = "expert"
            file_name = "TriviaExpert.csv"
        elif difficulty_choice == '4':
            display_category_options()
            return

        else:
            print("Invalid choice. Please select a valid difficulty level.")
            return

    elif choice == '2':
        if difficulty_choice == '1':
            difficulty = "easy"
            file_name = "Science.csv"
        elif difficulty_choice == '2':
            difficulty = "normal"
            file_name = "ScienceN.csv"
        elif difficulty_choice == '3':
            difficulty = "expert"
            file_name = "ScienceE.csv"
        elif difficulty_choice == '4':
            display_category_options()
            return
        else:
            print("Invalid choice. Please select a valid difficulty level.")
            return

    elif choice == '3':
        if difficulty_choice == '1':
            difficulty = "easy"
            file_name = "MathC.csv"
        elif difficulty_choice == '2':
            difficulty = "normal"
            file_name = "MathCNormal.csv"
        elif difficulty_choice == '3':
            difficulty = "expert"
            file_name = "MathCExpert.csv"
        elif difficulty_choice == '4':
            display_category_options()
            return
        else:
            print("Invalid choice. Please select a valid difficulty level.")
            return

    elif choice == '4':
        if difficulty_choice == '1':
            difficulty = "easy"
            file_name = "LiteraryTestEasy.csv"
        elif difficulty_choice == '2':
            difficulty = "normal"
            file_name = "LiteraryTestN.csv"
        elif difficulty_choice == '3':
            difficulty = "expert"
            file_name = "LiteraryTestE.csv"
        elif difficulty_choice == '4':
            display_category_options()
            return
        else:
            print("Invalid choice. Please select a valid difficulty level.")
            return

    elif choice == '5':
        if difficulty_choice == '1':
            difficulty = "easy"
            file_name = "History.csv"
        elif difficulty_choice == '2':
            difficulty = "normal"
            file_name = "HistoryN.csv"
        elif difficulty_choice == '3':
            difficulty = "expert"
            file_name = "HistoryE.csv"
        elif difficulty_choice == '4':
            display_category_options()
        else:
            print("Invalid choice. Please select a valid difficulty level.")
            return

    else:
        print("Invalid choice. Please select a valid option.")
        return

    print(f"\n--- {file_name.replace('.csv', '').replace('_', ' ').title()} - {difficulty.capitalize()} ---")

    questions = []
    with open(file_name, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['difficulty'].lower() == difficulty:
                questions.append((row['question'], row['answer']))

    game = MgaTanong(questions)
    score = game.start_quiz()
    random.shuffle(questions)

    game_over.play()
    save_results(pangalan, difficulty, file_name, score)
    print(f"Your results have been saved. Thank you for playing, {pangalan}!")

if __name__ == "__main__":
    while True:
        main()
        choice = input("Want to play? (yes/no): ").strip().lower()
        if choice == "no":
            pygame.quit()
            break