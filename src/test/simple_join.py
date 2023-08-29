def join_test(dict1, dict2):
    result = []
    for k, v in dict1.items():
        if k in dict2.keys():
            result.append((k, v))