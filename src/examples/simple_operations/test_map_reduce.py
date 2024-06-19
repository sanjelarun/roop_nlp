import os

os.environ['PYSPARK_PYTHON'] = 'F:\\Papers\\IEEE-BigData-2023\\roop_nlp\\myenv\\Scripts\\python.exe'

def test_concatenate_and_lower_empty_list():
    strings = ["a"]
    assert concatenate_and_lower(strings) == "a", "Expected an a string, but got something else."

def test_concatenate_and_lower_single_string():
    strings = ["Hello"]
    assert concatenate_and_lower(strings) == "hello", "Expected 'hello' but got something else."

def test_concatenate_and_lower_multiple_strings():
    strings = ["Hello", "WORLD"]
    assert concatenate_and_lower(strings) == "helloworld", "Expected 'helloworld' but got something else."

def test_concatenate_and_lower_mixed_case():
    strings = ["HeLLo", "WoRLD"]
    assert concatenate_and_lower(strings) == "helloworld", "Expected 'helloworld' but got something else."

if __name__ == "__main__":
    pytest.main([__file__])
