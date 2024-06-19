def concatenate_and_lower(strings):
    result = ''
    for str in strings:
        lower = str.lower()
        result += lower
    return result
