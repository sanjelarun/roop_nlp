def flatten_list_counter(list_of_lists):
    result = []
    for list in list_of_lists:
        for element in list:
            result.append(element)
    result = len(set(result))
    return result
