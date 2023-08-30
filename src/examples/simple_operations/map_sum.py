def square_and_sum(numbers):
    result = []
    s = 0
    for num in numbers:
        result.append(num ** 2)
        s = sum(result)
    return s
