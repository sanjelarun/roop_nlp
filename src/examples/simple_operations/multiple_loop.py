def even_filter(numbers):
    evens = []
    for num in numbers:
        if num % 2 == 0:
            evens.append(num)
    return evens

def length_counter(strings):
    lengths = []
    for s in strings:
        lengths.append(len(s))
    return lengths