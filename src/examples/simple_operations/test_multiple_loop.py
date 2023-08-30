import os
os.environ['PYSPARK_PYTHON'] = 'F:\\Papers\\IEEE-BigData-2023\\roop_nlp\\myenv\\Scripts\\python.exe'
# Tests for even_counter function

def test_even_counter_no_evens():
    numbers = [1, 3, 5, 7]
    assert even_filter(numbers) == [], f"Expected [] for input {numbers}, but got {even_filter(numbers)}"

def test_even_counter_all_evens():
    numbers = [2, 4, 6, 8]
    assert even_filter(numbers) == numbers, f"Expected {numbers} for input {numbers}, but got {even_filter(numbers)}"

def test_even_counter_mixed_numbers():
    numbers = [1, 2, 3, 4, 5]
    expected_result = [2, 4]
    assert even_filter(numbers) == expected_result, f"Expected {expected_result} for input {numbers}, but got {even_filter(numbers)}"


def test_length_counter_single_word():
    strings = ["apple"]
    expected_result = [5]
    assert length_counter(strings) == expected_result, f"Expected {expected_result} for input {strings}, but got {length_counter(strings)}"

def test_length_counter_multiple_words():
    strings = ["apple", "banana", "cherry"]
    expected_result = [5, 6, 6]
    assert length_counter(strings) == expected_result, f"Expected {expected_result} for input {strings}, but got {length_counter(strings)}"

if __name__ == "__main__":
    pytest.main([__file__])
