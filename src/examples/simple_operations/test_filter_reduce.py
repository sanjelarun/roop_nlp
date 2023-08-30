import os

os.environ['PYSPARK_PYTHON'] = 'F:\\Papers\\IEEE-BigData-2023\\roop_nlp\\myenv\\Scripts\\python.exe'

def test_sum_even_numbers_all_odd():
    assert sum_even_numbers([1, 3, 5, 7, 9]) == 0, "Expected 0 for a list of all odd numbers"

def test_sum_even_numbers_all_even():
    assert sum_even_numbers([2, 4, 6, 8, 10]) == 30, "Expected 30 for a list of 2, 4, 6, 8, 10"

def test_sum_even_numbers_mixed():
    assert sum_even_numbers([1, 2, 3, 4, 5]) == 6, "Expected 6 for a list of 1, 2, 3, 4, 5"

def test_sum_even_numbers_with_negatives():
    assert sum_even_numbers([-2, -4, -6, 2, 4, 6]) == 0, "Expected 0 for a list of -2, -4, -6, 2, 4, 6"

def test_sum_even_numbers_with_zero():
    assert sum_even_numbers([0, 1, 3, 5]) == 0, "Expected 0 for a list of 0, 1, 3, 5"

if __name__ == "__main__":
    pytest.main([__file__])