def flatten_list_counter(list_of_lists):
    result = []
    for sublist in list_of_lists:
        for item in sublist:
            result.append(item)
    result = len(result)
    return result
