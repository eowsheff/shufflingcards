import numpy as np
from collections import deque


def total_variation_distance(P: np.array, Q: np.array) -> float: # update type hinting for parameterd to allow deque
    if isinstance(P, deque):
        P = np.array(P)
    if isinstance(Q, deque):
        Q = np.array(Q)

    return 0.5 * np.sum(np.abs(P - Q))


def kl_divergence(P: np.array, Q: np.array) -> float: # update type hinting for parameterd to allow deque
    if isinstance(P, deque):
        P = np.array(P)
    if isinstance(Q, deque):
        Q = np.array(Q)

    return sum(P[i] * np.log2(P[i] / Q[i]) for i in range(len(P)))