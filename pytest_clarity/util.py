def direct_type_mismatch(lhs, rhs):
    return type(lhs) is not type(rhs)


def display_op_for(pytest_op):
    return "==" if pytest_op == "equal" else pytest_op
