import math
import numpy as np
from collections import deque


def eulerian(n: int, r: int) -> int:
    """
    This function returns the Eulerian number for n, according to the explicit formula, see here: https://en.wikipedia.org/wiki/Eulerian_number

    :param  n: total number of elements considered (0 to n).
            r: number of possible permutations with r ascents

    :return Eulerian number as an integer
    """
    if n < 0 or r < 0 or r >= n:
        return 0
    elif n == 0 and r == 0:
        return 1

    result = 0

    for i in range(0, r+1):
        result += ((-1)**i) * math.comb(n+1, i) * ((r-i)**n)

    return result


def uniform(n: int) -> float:
    return 1.0 / math.factorial(n)


def probability_rising_sequence(a, n, k, r):
    return math.comb(n-r+(a**k), n) / (a**(k*n))


def total_variation_distance(P: np.array, Q: np.array) -> float: # update type hinting for parameters to allow collections.deque
    """
    Given two collections.deques objects or two numpy.array objects (P and Q), this function calculates the Total Variation Distance (TVD)
    between the two objects, as used by Diaconis et al. (1992). See for reference: https://shorturl.at/PQX38 
    The two arrays, represent two distributions. 
    The function returns a float which represents the TVD value between the two distributions P and Q.

    Note: if either object, P or Q is a collections.deque object, this function will first convert it into a numpy.array

    :param  P: numpy.array or collections.deque which holds a sequence of probabilities (float), and represents a probability distribution
            Q: numpy.array or collections.deque which holds a sequence of probabilities (float), and represents a probability distribution

    :return float representing the TVD between the two distributions P and Q
    """
    if isinstance(P, deque) or isinstance(P, list):
        P = np.asarray(P)
    if isinstance(Q, deque) or isinstance(P, list):
        Q = np.asarray(Q)

    return 0.5 * np.sum(np.abs(P - Q))


def kl_divergence(P: np.array, Q: np.array) -> float: # update type hinting for parameters to allow deque
    """
    Given two collections.deques objects or two numpy.array objects (P and Q), this function calculates the Kullback-Leibler (KL) divergence 
    between P and Q. given Q; D(P || Q). For reference about the KL divergence, see: https://shorturl.at/ilwN0
    The two arrays, represent two distributions.
    The function returns a float which represents the KL divergence value between the two distributions P and Q.

    Note: if either object, P or Q is a collections.deque object, this function will first convert it into a numpy.array

    :param  P: numpy.array or collections.deque which holds a sequence of probabilities (float), and represents a probability distribution
            Q: numpy.array or collections.deque which holds a sequence of probabilities (float), and represents a probability distribution

    :return float representing the KL divergence between the two distributions P and Q
    """
    if isinstance(P, deque) or isinstance(P, list):
        P = np.asarray(P)
    if isinstance(Q, deque) or isinstance(P, list):
        Q = np.asarray(Q)

    return np.sum(P * np.log2(P / Q))