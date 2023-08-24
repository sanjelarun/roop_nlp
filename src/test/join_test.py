import pytest
from join import join_list

def test_join_list_empty_lists():
    orders = []
    order_details = []
    assert join_list(orders, order_details) == [], "Expected an empty list"

def test_join_list_empty_orders():
    orders = []
    order_details = [(1, 'detail1'), (2, 'detail2')]
    assert join_list(orders, order_details) == [], "Expected an empty list"

def test_join_list_empty_order_details():
    orders = [(1, 'order1'), (2, 'order2')]
    order_details = []
    assert join_list(orders, order_details) == [], "Expected an empty list"

def test_join_list_no_matches():
    orders = [(1, 'order1'), (2, 'order2')]
    order_details = [(3, 'detail3'), (4, 'detail4')]
    assert join_list(orders, order_details) == [], "Expected an empty list"

def test_join_list_with_matches():
    orders = [(1, 'order1'), (2, 'order2')]
    order_details = [(1, 'detail1'), (2, 'detail2'), (3, 'detail3')]
    expected_result = [(1, 'order1', 'detail1'), (2, 'order2', 'detail2')]
    assert join_list(orders, order_details) == expected_result, f"Expected {expected_result}, but got {join_list(orders, order_details)}"

if __name__ == "__main__":
    pytest.main([__file__])
