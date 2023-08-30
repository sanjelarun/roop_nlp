def test_flatten_list_single_element_sublists():
    assert flatten_list_counter([[1], [2], [3]]) == 3

def test_flatten_list_multiple_element_sublists():
    assert flatten_list_counter([[1, 2], [3, 4], [5, 6]]) == 6

def test_flatten_list_mixed_length_sublists():
    assert flatten_list_counter([[1], [2, 3], [4, 5, 6]]) == 6

def test_flatten_list_single_sublist():
    assert flatten_list_counter([[1, 2, 3, 4, 5]]) == 5

def test_flatten_list_non_integer_elements():
    assert flatten_list_counter([['a'], ['b', 'c'], [1, 2]]) == 5