def dict_difference(dict1, dict2):
    """
    Returns the difference between `dict1` and `dict2`, i.e. `dict1` without items in `dict2`.
    """
    return {key: value for key, value in dict1.iteritems() if key not in dict2}


def dict_intersection(dict1, dict2):
    """
    Returns the intersection of two dictionaries. Intersections are judged based on keys, not values.
    """
    return {key: value for key, value in dict1.iteritems() if key in dict2}


def dicts_intersect(dict1, dict2):
    """
    Returns `True` if two dictionaries have interesecting keys.
    """
    return len(dict_intersection(dict1, dict2)) > 0
