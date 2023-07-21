import numpy as np
from collections import deque

# TODO: add doc strings

def total_variation_distance(P: np.array, Q: np.array) -> float: # update type hinting for parameters to allow deque
    """
    Given two collections.deques objects or two numpy.array objects (P and Q), this function calculates the Total Variation Distance (TVD)
    between the two objects, as used by Diaconis et al. (1992). See for reference: https://shorturl.at/PQX38 
    The two arrays, represent two distributions. 
    The function returns a float which represents the TVD value between the two distributions P and Q.

    Note: if either object, P or Q is a collections.deque object, this function will first convert it into a numpy.array

    :param  P: numpy.array or collections.deque which holds a sequence of numbers (int), and represents a distribution
            Q: numpy.array or collections.deque which holds a sequence of numbers (int), and represents a distribution

    :return float representing the TVD between the two distributions P and Q
    """
    if isinstance(P, deque):
        P = np.array(P)
    if isinstance(Q, deque):
        Q = np.array(Q)

    return 0.5 * np.sum(np.abs(P - Q))


def kl_divergence(P: np.array, Q: np.array) -> float: # update type hinting for parameters to allow deque
    """
    Given two collections.deques objects or two numpy.array objects (P and Q), this function calculates the Kullback-Leibler (KL) divergence 
    between the two objects. For reference about the KL divergence, see: https://shorturl.at/ilwN0
    The two arrays, represent two distributions. 
    The function returns a float which represents the KL divergence value between the two distributions P and Q.

    Note: if either object, P or Q is a collections.deque object, this function will first convert it into a numpy.array

    :param  P: numpy.array or collections.deque which holds a sequence of numbers (int), and represents a distribution
            Q: numpy.array or collections.deque which holds a sequence of numbers (int), and represents a distribution

    :return float representing the KL divergence between the two distributions P and Q
    """
    if isinstance(P, deque):
        P = np.array(P)
    if isinstance(Q, deque):
        Q = np.array(Q)

    return sum(P[i] * np.log2(P[i] / Q[i]) for i in range(len(P)))