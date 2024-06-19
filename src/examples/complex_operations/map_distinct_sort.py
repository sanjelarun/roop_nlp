
def map_sort(numbers):
    result = []
    for num in numbers:
        result.append(num * 2)
    result = list(set(result))
    result = result.sort()
    return result