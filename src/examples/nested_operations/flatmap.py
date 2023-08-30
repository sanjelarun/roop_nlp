def flatten_list(list_of_lists):
    result = []
    for sublist in list_of_lists:
        for item in sublist:
            result.append(item)
    return result
