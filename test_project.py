from unittest.mock import MagicMock, patch
import pytest
import os
import csv
import tkinter as tk
from project import QuizGame

def test_name_validation_with_special_characters(quiz_game):
    with patch('tkinter.simpledialog.askstring', return_value='Invalid@Name'):
        with patch('tkinter.messagebox.showwarning') as mock_showwarning:
            quiz_game.start_quiz()
            mock_showwarning.assert_called_once_with("Warning", "You need to enter a valid name (no special characters)!")

@pytest.fixture
def setup_test_file():
    test_file = 'test_questions.csv'
    with open(test_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['question', 'answer', 'difficulty'])
        writer.writerow(['What is 2 + 2?', '4', 'Easy'])
        writer.writerow(['What is the capital of France?', 'Paris', 'Easy'])
    yield test_file
    if os.path.exists(test_file):
        os.remove(test_file)

@pytest.fixture
def quiz_game(setup_test_file):
    root = tk.Tk()
    game = QuizGame(root)
    yield game
    root.destroy()

@pytest.fixture
def quiz_game():
    game = QuizGame(MagicMock())
    game.questions = [("What is the capital of France?", "Paris")]
    game.current_question_index = 0
    game.lives = 3
    return game

def test_hint_retrieval_and_display(quiz_game):
    with patch('tkinter.messagebox.showinfo') as mock_showinfo:
        quiz_game.give_hint()
        mock_showinfo.assert_called_once_with("Hint", "Hint: P...\nLives left: 2")

def test_life_deduction(quiz_game):
    quiz_game.give_hint()
    assert quiz_game.lives == 2

def test_no_lives_left_warning(quiz_game):
    quiz_game.lives = 0
    with patch('tkinter.messagebox.showwarning') as mock_showwarning:
        quiz_game.give_hint()
        mock_showwarning.assert_called_once_with("No Lives Left", "You have no lives left to use a hint.")

def test_check_answer_correct(quiz_game):
    quiz_game.questions = [("What is 2 + 2?", "4")]
    quiz_game.score = 0
    quiz_game.lives = 3
    quiz_game.consecutive_correct = 0

    with patch("tkinter.messagebox.showinfo") as mock_showinfo:
        quiz_game.check_answer("4", "4")

        assert quiz_game.score == 1
        assert quiz_game.lives == 3
        assert quiz_game.consecutive_correct == 1

        mock_showinfo.assert_called_once_with("Correct!", "Correct!")

def test_check_answer_wrong(quiz_game):
    quiz_game.questions = [("What is 2 + 2?", "4")]
    quiz_game.score = 0
    quiz_game.lives = 3

    with patch('tkinter.messagebox.showinfo') as mock_showinfo:
        quiz_game.check_answer("5", "4")

        assert quiz_game.score == 0
        assert quiz_game.lives == 2
        mock_showinfo.assert_called_once_with("Wrong!", "Wrong! The answer is: 4")

if __name__ == '__main__':
    pytest.main()
