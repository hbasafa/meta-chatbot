

def get_difference(list1, list2):
    diffs = [v for v in list1 if v not in list2]
    return diffs


def get_key(dictionary):
    [key] = dictionary.keys()
    return key
