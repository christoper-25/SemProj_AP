import pytest

from project import display_leaderboards
from project import display_category_options
from project import display_difficulty_options
from project import save_results

def test_save_results():
    data = [  "Trivia.csv", ]
    save_results("Greg","Easy", 'quiz_results.csv',9)

    with open('quiz_results.csv', 'r') as s:
        content = s.read()
        assert "Greg" in content
        assert "Easy" in content
        assert "Trivia.csv" in content
        assert "9" in content
def test_display_difficulty_options(capsys):
    # Test if difficulty options are displayed correctly
    display_difficulty_options()
    captured = capsys.readouterr()
    assert "Easy" in captured.out
    assert "Normal" in captured.out
    assert "Expert" in captured.out
    assert "Back" in captured.out
def test_display_category_options(capsys):
    display_category_options()
    captured = capsys.readouterr()
    assert "1. Trivia Test" in captured.out
    assert "2. Science Test" in captured.out
    assert "3. Math Test" in captured.out
    assert "4. Literary Test" in captured.out
    assert "5. History Test" in captured.out
    assert "6. Display Leaderboards" in captured.out
    assert "7. Exit" in captured.out
