data = [1, 2, 3, 4, 5]
squared = [num * num for num in data]

matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
sums = []
for row in matrix:
    row_sum = 0
    for item in row:
        row_sum += item
    sums.append(row_sum)
