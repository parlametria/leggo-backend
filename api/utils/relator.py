import numpy as np


def check_relator_id(value):
    if np.isnan(value):
        value = None
    else:
        value = int(value)
        return value
