


# Test with single-element lists
def test_single_element_lists():
    assert union_and_count([1], [2]) == 2

# Test with multi-element lists with distinct elements
def test_distinct_elements():
    assert union_and_count([1, 2], [3, 4]) == 4

# Test with multi-element lists with overlapping elements
def test_overlapping_elements():
    assert union_and_count([1, 2], [2, 3]) == 4

# Test with all zeros
def test_all_zeros():
    assert union_and_count([0, 0], [0, 0]) == 4

# Test with negative numbers
def test_negative_numbers():
    assert union_and_count([-1, -2], [-20, -3,123,98]) == 6

if __name__ == '__main__':
    pytest.main([__file__])