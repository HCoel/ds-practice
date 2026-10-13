import math


def trimmed_mean(values: list[float], proportion: float = 0.1) -> float:
    """Mean after dropping the lowest and highest `proportion` of values."""
    if not values:
        raise ValueError("empty")
    if proportion < 0 or proportion >= 0.5:
        raise ValueError

    sorted_values = sorted(values)
    k = math.floor(proportion * len(values))
    if k == 0:
        trimmed_values = sorted_values
    else:
        trimmed_values = sorted_values[k:-k]

    return math.fsum(trimmed_values) / len(trimmed_values)

    # TODO 3: slice off k from each end and return the mean (math.fsum is precise)
    raise NotImplementedError
