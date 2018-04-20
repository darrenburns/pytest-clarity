from collections import Sized, Iterable


def auto_repr(item):
    """
    Recurse through an instance, constructing a string representation
    :param item: any object
    :return: a best guess string representation of the object
    """
    if has_overriden_repr(item):
        return repr(item)

    output = type(item).__name__ + '('
    try:
        variables = vars(item).items()
    except TypeError:
        return repr(item)

    for i, var in enumerate(variables):
        output += var[0] + '=' + auto_repr(var[1])
        if i != len(variables) - 1:
            output += ', '

    return output + ')'


def display_op_for(pytest_op):
    return '==' if pytest_op == 'equal' else pytest_op


def has_overriden_repr(item):
    return not type(item).__repr__ is object.__repr__


def _possibly_missing_eq(lhs, rhs):
    try:
        left_dict, right_dict = vars(lhs), vars(rhs)
    except TypeError:
        return False

    return all([
        isinstance(lhs, type(rhs)),
        lhs != rhs,
        left_dict == right_dict,
    ])


def _has_differing_len(lhs, rhs):
    if isinstance(lhs, Sized) and isinstance(rhs, Sized):
        return len(lhs) != len(rhs)
    return False


def _is_iterable(x):
    return isinstance(x, Iterable)