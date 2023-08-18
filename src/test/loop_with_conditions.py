data = [1, 2, 3, 4, 5]
results = []
for num in data:
    if num % 2 == 0:
        results.append(num * 2)
    else:
        results.append(num + 1)
