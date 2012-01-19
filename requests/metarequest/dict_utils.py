def copy_dict_except(source, except_keys):
    """
    Copies a dictionary into a new dictionary, but leaves out any keys in the `except_keys` list.
    """
    new_dict = {}
    for key, value in source.iteritems():
        if key not in except_keys:
            new_dict[key] = value

    return new_dict


def dict_intersection(dict1, dict2):
    """
    Returns the intersection of two dictionaries. Intersections are judged based on keys, not values.
    """
    return {key: value for key, value in dict1.iteritems()
            if key in dict2}


def dicts_intersect(dict1, dict2):
    """
    Returns `True` if two dictionaries have interesecting keys.
    """
    return len(dict_intersection(dict1, dict2)) > 0
