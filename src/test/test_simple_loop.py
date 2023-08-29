import os
os.environ['PYSPARK_PYTHON'] = 'F:\\Papers\\IEEE-BigData-2023\\roop_nlp\\myenv\\Scripts\\python.exe'


def test_total_empty_list():
    data = []
    assert total(data) == 0, f"Expected 0 for input {data}, but got {total(data)}"

def test_total_single_element():
    data = [5]
    expected_result = 5 * 2
    assert total(data) == expected_result, f"Expected {expected_result} for input {data}, but got {total(data)}"

def test_total_multiple_elements():
    data = [1, 2, 3, 4, 5]
    expected_result = sum([x*2 for x in data])
    assert total(data) == expected_result, f"Expected {expected_result} for input {data}, but got {total(data)}"

def test_total_negative_numbers():
    data = [-1, -2, -3]
    expected_result = sum([x*2 for x in data])
    assert total(data) == expected_result, f"Expected {expected_result} for input {data}, but got {total(data)}"

def test_total_mixed_numbers():
    data = [-1, 2, -3, 4, -5]
    expected_result = sum([x*2 for x in data])
    assert total(data) == expected_result, f"Expected {expected_result} for input {data}, but got {total(data)}"

if __name__ == "__main__":
    pytest.main([__file__])
