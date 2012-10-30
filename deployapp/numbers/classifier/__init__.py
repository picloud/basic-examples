
def classify(values):
    """*values* should be a list of numbers. Returns a list of the
    same size with values 'even' or 'odd'."""

    return ['odd' if value % 2 else 'even' for value in values]

