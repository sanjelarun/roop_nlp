def flatted_filter(list_of_lists):
    result = []
    for sublist in list_of_lists:
        for num in sublist:
            if num > 10:
                result.append(num)
    result = result.sort()
    return result