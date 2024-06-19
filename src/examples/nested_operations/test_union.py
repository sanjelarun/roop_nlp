
def test_combine_two_non_empty_lists():
    assert combine_two_lists(["a", "b"], ["c", "d"]) == ["a", "b", "c", "d"]

def test_combine_first_list_empty():
    assert combine_two_lists([1], ["c", "d"]) == [1,"c", "d"]

def test_combine_second_list_empty():
    assert combine_two_lists(["a", "b"], [1]) == ["a", "b", 1]

