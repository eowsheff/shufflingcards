import math
import numpy as np
from collections import deque


def get_random_sequence(first_element: int, last_element: int, random_seed: int = None) -> np.array:
    """
    This function creates a sequence of n elements, without replacement, from `first_element` (included) to `last_element` (included).
    It samples these elements from a uniform distribution, meaning each element is picked with equal probability.

    E.g.: to create a random sequence of numbers, ranging from 1 (included) to 52 (inclued), this function is called as:
        get_random_sequence(1, 52)
        This will produce a list with random numbers such as: [3, 1, 52, .... , 14]


    :param  first_element: integer, indicating the first number in the sequence
            last_element: integer, indicating the last number in the sequence
            random_seed: integer which sets a random seed to np.random.seed, this allows reproductin the same results when the function is repeated

    :return np.array, containting n elements, samples from a uniform distribution, without replacement
    """
    np.random.seed(random_seed)

    n_elem = range(first_element, last_element + 1)
    n = last_element - (first_element - 1)
    return np.random.choice(n_elem, n, replace=False)


def eulerian(n: int, k: int) -> int:
    """
    This function returns the Eulerian number for n, according to the explicit formula here: https://en.wikipedia.org/wiki/Eulerian_number

    :param  n: total number of elements considered (0 to n).
            k: number of possible permutations with k ascents

    :return Eulerian number as an integer
    """
    if n < 0 or k < 0:
        return 0
    elif n == 0 and k == 0:
        return 1
    elif n <= k:
        return 0

    result = 0
    sign = 1

    for i in range(0, k+1):
        result += sign * math.comb(n+1, i) * ((k+1-i)**n)
        sign = sign * (-1)

    return result


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
    if isinstance(P, deque):
        P = np.asarray(P)
    if isinstance(Q, deque):
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
    if isinstance(P, deque):
        P = np.asarray(P)
    if isinstance(Q, deque):
        Q = np.asarray(Q)

    return sum(P[i] * np.log2(P[i] / Q[i]) for i in range(len(P)))