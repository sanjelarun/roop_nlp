def test_flatted_filter_basic_case():
    assert flatted_filter([[11, 12], [10, 9], [13, 14]]) == [11, 12, 13, 14]

def test_flatted_filter_all_less_than_ten():
    assert flatted_filter([[1, 2], [3, 4]]) == []

def test_flatted_filter_with_ten():
    assert flatted_filter([[11, 10], [9, 10]]) == [11]

def test_flatted_filter_single_element_sublists():
    assert flatted_filter([[11], [12], [10]]) == [11, 12]