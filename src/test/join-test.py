# Sample data: two lists of tuples where the first item is the 'key'
orders = [(1, 'Apple'), (2, 'Banana'), (3, 'Cherry')]
order_details = [(1, 'Fruit'), (2, 'Fruit'), (3, 'Berry'), (4, 'Unknown')]

# The result will hold tuples combining matched orders and order details
joined_result = []

for order in orders:
    for detail in order_details:
        if order[0] == detail[0]:  # Join on the first item (key) of each tuple
            joined_result.append((order[0], order[1], detail[1]))
