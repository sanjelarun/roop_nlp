import os
os.environ['PYSPARK_PYTHON'] = 'F:\\Papers\\IEEE-BigData-2023\\roop_nlp\\myenv\\Scripts\\python.exe'

# def test_join_list_empty_lists():
#     orders = []
#     order_details = []
#     assert join_list(orders, order_details) == [], "Expected an empty list"

# def test_join_list_empty_orders():
#     orders = []
#     order_details = [(1, 'detail1'), (2, 'detail2')]
#     assert join_list(orders, order_details) == [], "Expected an empty list"

def test_join_list_empty_order_details():
    orders = [(1, 'order1'), (2, 'order2')]
    order_details = []
    assert join_list(orders, order_details).collect() == [], "Expected an empty list"

def test_join_list_no_matches():
    orders = [(1, 'order1'), (2, 'order2')]
    order_details = [(3, 'detail3'), (4, 'detail4')]
    assert join_list(orders, order_details).collect() == [], "Expected an empty list"

def test_join_list_with_matches():
    orders = [(1, 'order1'), (2, 'order2')]
    order_details = [(1, 'detail1'), (2, 'detail2'), (3, 'detail3')]
    expected_result = sorted([(1, ('order1', 'detail1')), (2, ('order2', 'detail2'))])
    
    # Sorting the actual result
    actual_result = sorted(join_list(orders, order_details).collect())

    assert actual_result == expected_result, f"Expected {expected_result}, but got {actual_result}"


if __name__ == "__main__":
    pytest.main([__file__])
