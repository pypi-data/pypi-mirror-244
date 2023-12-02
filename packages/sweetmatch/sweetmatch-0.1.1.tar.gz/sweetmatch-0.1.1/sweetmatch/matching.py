from scipy.optimize import linear_sum_assignment
from typing import Callable, Optional, TypeVar
import numpy as np


T = TypeVar("T")
U = TypeVar("U")


def match(x:list[T], y:list[U], cost_function:Callable[[T, U], float], cost_threshold:Optional[float]=None) -> list[tuple[T, U]]:
    
    cost_matrix = np.zeros((len(x), len(y)))

    for i in range(len(x)):
        for j in range(len(y)):
            cost_matrix[i,j] = cost_function(x[i], y[j])

    raw_matches = linear_sum_assignment(cost_matrix)

    matches: list[tuple[T, U]] = []
    for i, j in zip(raw_matches[0], raw_matches[1]):
        if cost_threshold is not None:
            if cost_matrix[i, j] > cost_threshold: 
                continue
        matches.append((x[i], y[j]))

    return matches
