data0 = [1, 2, 3, 4, 5]
for i in range(len(data0)):
    data0[i] *= 3

list0 = [1, 2, 3]
results = []
for element in list0:
    results.append(element**3)

numbers = [10, 20, 30]
result = []
for num in numbers:
    result.append(num * 2)

strings = ["HELLO", "WORLD"]
result_str = ''
for str in strings:
    result_str += str.lower()

even_result = []
for num in numbers:
    if num % 2 == 0:
        even_result.append(num * 2)
