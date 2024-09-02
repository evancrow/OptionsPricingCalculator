import pytest
from Helpers.inputs import integer_input, float_input, string_input, make_options_input_prompt, options_input

# MARK: integer_input
def test_integer_input_valid_input(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: "1")
    assert integer_input("Enter a number") == 1

def test_integer_input_invalid_input(monkeypatch, capsys):
    inputs = iter(["not a number", "42"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))

    result = integer_input("Enter a number: ")

    captured = capsys.readouterr()
    assert "Please enter a number." in captured.out
    assert result == 42

# MARK: float_input
def test_float_input_valid_input(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: "1.5")
    assert float_input("Enter a number") == 1.5

def test_float_input_invalid_input(monkeypatch, capsys):
    inputs = iter(["not a number", "42.5"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))

    result = float_input("Enter a number: ")

    captured = capsys.readouterr()
    assert "Please enter a number." in captured.out
    assert result == 42.5

# MARK: string_input
def test_string_input_valid_input(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: "test string")
    assert string_input("Enter a string") == "test string"

def test_string_input_integer_input(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: "1")
    assert string_input("Enter a string") == "1"

# MARK: make_options_input_prompt
def test_make_options_input_prompt():
    options = ["A", "B", "C"]
    assert make_options_input_prompt(options) == "Choose from the following options: A, B, C "

def test_make_options_input_prompt_no_options():
    assert make_options_input_prompt([]) == None

# MARK: options_input
def test_options_input_valid_option(monkeypatch):
    options = ["A", "B", "C"]
    monkeypatch.setattr('builtins.input', lambda _: "B")
    result = options_input(options)
    assert result == "B"

def test_options_input_case_insensitive_input(monkeypatch):
    options = ["A", "B", "C"]
    monkeypatch.setattr('builtins.input', lambda _: "c")
    result = options_input(options)
    assert result == "c"

def test_options_input_invalid_then_valid_option(monkeypatch):
    options = ["X", "Y", "Z"]
    inputs = iter(["W", "Y"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    result = options_input(options)
    assert result == "Y"

def test_options_input_empty_options_list():
    result = options_input([])
    assert result is None

def test_options_input_invalid_option_message(capsys, monkeypatch):
    options = ["A", "B"]
    inputs = iter(["C", "A"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    options_input(options)
    captured = capsys.readouterr()
    assert "Invalid choice." in captured.out