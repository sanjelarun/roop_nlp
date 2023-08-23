def join_list(orders, order_details):
    # The result will hold tuples combining matched orders and order details
    joined_result = []

    for order in orders:
        for detail in order_details:
            if order[0] == detail[0]:  # Join on the first item (key) of each tuple
                joined_result.append((order[0], order[1], detail[1]))
    return joined_result