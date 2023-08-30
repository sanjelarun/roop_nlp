def test_map_sort_basic_case():
    assert map_sort([1, 2, 3]) == [2, 4, 6]

def test_map_sort_with_zero():
    assert map_sort([0, 1, 2]) == [0, 2, 4]

def test_map_sort_negative_numbers():
    assert map_sort([-1, -2, -3]) == [-6, -4, -2]

def test_map_sort_mixed_numbers():
    assert map_sort([-1, 0, 1]) == [-2, 0, 2]

def test_map_sort_with_duplicates():
    assert map_sort([1, 1, 2]) == [2, 4]

def test_map_sort_non_integer():
    assert map_sort([1.5, 2.5, 3.5]) == [3.0, 5.0, 7.0]