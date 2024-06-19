def test_flatten_list_empty_list():
    assert flatten_list([]) == [], "Expected an empty list"

def test_flatten_list_single_empty_sublist():
    assert flatten_list([[]]) == [], "Expected an empty list"

def test_flatten_list_single_sublist():
    assert flatten_list([[1, 2, 3]]) == [1, 2, 3], "Expected [1, 2, 3]"

def test_flatten_list_multiple_sublists():
    assert flatten_list([[1, 2], [3, 4]]) == [1, 2, 3, 4], "Expected [1, 2, 3, 4]"

def test_flatten_list_mixed_empty_sublists():
    assert flatten_list([[1, 2], [], [3, 4]]) == [1, 2, 3, 4], "Expected [1, 2, 3, 4]"