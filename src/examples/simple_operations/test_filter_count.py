
def test_count_positive_values_empty_list():
    assert count_positive_values([-2]) == 0, "Expected 0 for an empty list"

def test_count_positive_values_all_negatives():
    assert count_positive_values([-1, -2, -3]) == 0, "Expected 0 for a list with all negatives"

def test_count_positive_values_with_zero():
    assert count_positive_values([0]) == 0, "Expected 0 for a list with zero"

def test_count_positive_values_all_positives():
    assert count_positive_values([1, 2, 3]) == 3, "Expected 3 for a list with all positives"

def test_count_positive_values_mixed_values():
    assert count_positive_values([-1, 0, 1, 2]) == 2, "Expected 2 for a list with mixed values"
