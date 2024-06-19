
def test_square_and_sum_single_element():
    assert square_and_sum([3]) == 9, "Expected 9 for a list with a single element 3"

def test_square_and_sum_multiple_elements():
    assert square_and_sum([1, 2, 3]) == 14, "Expected 14 for a list of 1, 2, 3"

def test_square_and_sum_with_negatives():
    assert square_and_sum([-1, -2, 3]) == 14, "Expected 14 for a list of -1, -2, 3"

def test_square_and_sum_with_zero():
    assert square_and_sum([0, 3, 4]) == 25, "Expected 25 for a list of 0, 3, 4"