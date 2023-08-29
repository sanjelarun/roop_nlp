from pyspark import SparkContext, SparkConf

def get_or_create_spark_context():
    conf = SparkConf().setAppName('MyApp').setMaster('local[2]')
    return SparkContext.getOrCreate(conf)

def even_counter(numbers):
    evens = []
    for num in numbers:
        if num % 2 == 0:
            evens.append(num)
    return evens

def length_counter(strings):
    lengths = []
    sc = get_or_create_spark_context()
    strings_rdd = sc.parallelize(strings)
    lengths = strings_rdd.map(lambda s: len(s)).collect()
    sc.stop()
    return lengths
import pytest


import os
os.environ['PYSPARK_PYTHON'] = 'F:\\Papers\\IEEE-BigData-2023\\roop_nlp\\myenv\\Scripts\\python.exe'
# Tests for even_counter function
def test_even_counter_empty_list():
    numbers = []
    assert even_counter(numbers) == [], f"Expected [] for input {numbers}, but got {even_counter(numbers)}"

def test_even_counter_no_evens():
    numbers = [1, 3, 5, 7]
    assert even_counter(numbers) == [], f"Expected [] for input {numbers}, but got {even_counter(numbers)}"

def test_even_counter_all_evens():
    numbers = [2, 4, 6, 8]
    assert even_counter(numbers) == numbers, f"Expected {numbers} for input {numbers}, but got {even_counter(numbers)}"

def test_even_counter_mixed_numbers():
    numbers = [1, 2, 3, 4, 5]
    expected_result = [2, 4]
    assert even_counter(numbers) == expected_result, f"Expected {expected_result} for input {numbers}, but got {even_counter(numbers)}"

# Tests for length_counter function
def test_length_counter_empty_list():
    strings = []
    assert length_counter(strings) == [], f"Expected [] for input {strings}, but got {length_counter(strings)}"

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