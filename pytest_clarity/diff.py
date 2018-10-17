import difflib

from pytest_clarity.output import Colour, deleted_text, inserted_text, non_formatted


def build_split_diff(lhs_repr, rhs_repr):
    lhs_out, rhs_out = "", ""

    matcher = difflib.SequenceMatcher(None, lhs_repr, rhs_repr)
    for op, i1, i2, j1, j2 in matcher.get_opcodes():

        lhs_substring_lines = lhs_repr[i1:i2].splitlines()
        rhs_substring_lines = rhs_repr[j1:j2].splitlines()

        for i, lhs_substring in enumerate(lhs_substring_lines):
            if op == "replace":
                lhs_out += inserted_text(lhs_substring)
            elif op == "delete":
                lhs_out += inserted_text(lhs_substring)
            elif op == "insert":
                lhs_out += Colour.stop + lhs_substring
            elif op == "equal":
                lhs_out += Colour.stop + lhs_substring

            if i != len(lhs_substring_lines) - 1:
                lhs_out += "\n"

        for j, rhs_substring in enumerate(rhs_substring_lines):
            if op == "replace":
                rhs_out += deleted_text(rhs_substring)
            elif op == "insert":
                rhs_out += deleted_text(rhs_substring)
            elif op == "equal":
                rhs_out += Colour.stop + rhs_substring

            if j != len(rhs_substring_lines) - 1:
                rhs_out += "\n"

    return lhs_out.splitlines(), rhs_out.splitlines()


def build_unified_diff(lhs_repr, rhs_repr):
    differ = difflib.Differ()
    lines_lhs, lines_rhs = lhs_repr.splitlines(), rhs_repr.splitlines()
    diff = differ.compare(lines_lhs, lines_rhs)

    output = []
    for line in diff:
        # Differ instructs us how to transform left into right, but we want
        # our colours to indicate how to transform right into left
        if line.startswith("- "):
            output.append(inserted_text(" L " + line[2:]))
        elif line.startswith("+ "):
            output.append(deleted_text(" R " + line[2:]))
        elif line.startswith("? "):
            # We can use this to find the index of change in the
            # line above if required in the future
            pass
        else:
            output.append(non_formatted(line))

    return output
