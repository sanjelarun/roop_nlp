def count_positive_values(values):
    result = []
    for val in values:
        if val > 0:
            result.append(val)
        cnt = len(result)
    return cnt