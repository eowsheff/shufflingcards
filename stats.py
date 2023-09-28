import math
import numpy as np
import pandas as pd
from deck import Deck


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
    """
    Function which returns a value according to the uniform distribution
    """
    return 1.0 / math.factorial(n)


def probability_rising_sequence(a: int, n: int, k: int, r: int) -> float:
    """
    Calculate the probability of obtaining r rising sequences, when performing k a-shuffles, on a deck of n cards, with a packets.

    :param  a: number of packets in the a-shuffle
            n: number of cards in a deck
            k: number of shuffles
            r: number of rising sequences
    
    :return probability of getting r rising sequences
    """
    return math.comb(n-r+(a**k), n) / (a**(k*n))


def theoretical_total_variation_distance_riffle_shuffle(a: int, n: int, k: int, r: int, uniform_probability: float) -> float:
    """
    Calculate theoretical TVD based on a packets, n cars, k shuffles and r rising sequences. Compare versus uniform_probability

    Returns TVD as float
    """

    var_distance: float = 0

    for r in range(1, n+1):
        eul: int = eulerian(n, r)
        prob_r: float = probability_rising_sequence(a, n, k, r)
        if eul > 0:
            var_distance += eul * abs(prob_r - uniform_probability)
        
    return var_distance / 2


def find_consecutive_sequences(deck: Deck, sequence_length: int): # not used in dissertation due to unreliable results
    """
    Given a deck of cards (input parameter `deck`), this function calculates the number of consecutive subsequent cards with length `sequence_length`.
    
    It returns a list with the sequences with consecutive numbers of length the sequence_length
    Thus, given a deck [1,2,3,4,7,8,6] the function returns a list: [[1,2,3] [2,3,4]]

    :param  deck, Deck object, representing a card deck
            sequence_length, the length of the sequences to find

    :return list of of lists. Each inner-list containing a sequence of subsequent numbers
    """
    
    consecutive_sequences:list = []
    
    # Check if there are enough numbers to form a sequence
    if len(deck) < sequence_length:
        return consecutive_sequences

    for i in range(len(deck) - sequence_length + 1):
        is_sequence = True
        for j in range(1, sequence_length):
            if deck[i+j] - deck[i+j-1] != 1:
                is_sequence = False
                break

        if is_sequence:
            consecutive_sequences.append(tuple(deck[i:i+sequence_length]))
            
    return consecutive_sequences
    

def extract_decks_per_shuffle_number(results: list, shuffle_number: int) -> list:
    """
    Extract the shuffled decks for a specific shuffle from each trial
    """
    return [trial[shuffle_number + 1] for trial in results]


def create_frequency_matrix(results: list) -> pd.DataFrame:
    """
    Create big frequency matrix, showing which cards landed on which position in the deck, for each trial.
    """
    n_cards: int = len(results[0])
    unique_cards: list = [c for c in range(1,  n_cards + 1)]

    matrix: np.array = np.zeros((n_cards, n_cards))

    for deck in results:
        for idx, card in enumerate(deck):
            row = unique_cards.index(card)
            matrix[row][idx] += 1

    matrix: np.array = matrix.astype(int)

    df: pd.DataFrame = pd.DataFrame(matrix)
    df.columns += 1
    df.index += 1
    
    return df


def winding_distance(deck: Deck, card: int):
    predecessor: int = card - 1 if card > 1 else max(deck)
    successor: int = card + 1 if card < max(deck) else 1

    # Distance from predecessor to card
    pre_to_elem: int = 0
    i = deck.index(predecessor)
    while deck[i] != card:
        pre_to_elem += 1
        i = (i + 1) % len(deck)
        
    # Distance from element to card
    elem_to_suc: int = 0
    while deck[i] != successor:
        elem_to_suc += 1
        i = (i + 1) % len(deck)
    
    return pre_to_elem + elem_to_suc - 1 